"""Tax Case + Service Request + Triage routes (jsonl MVP store)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(tags=["cases-services"])

# ROOT = monorepo root (apps/api/app -> parents[3])
ROOT = Path(__file__).resolve().parents[3]
CASE_STORE = ROOT / "data" / "tax_cases.jsonl"
SERVICE_STORE = ROOT / "data" / "service_requests.jsonl"

SERVICE_CATALOG: list[dict[str, str]] = [
    {"code": "S01", "title": "سؤال سریع مالیاتی", "path": "AI + RAG"},
    {"code": "S02", "title": "تحلیل پرونده", "path": "Tax Case + Document AI"},
    {"code": "S03", "title": "تحلیل برگ تشخیص / مطالبه", "path": "Case + Risk"},
    {"code": "S04", "title": "تهیه لایحه", "path": "AI draft + Expert"},
    {"code": "S05", "title": "اعتراض مالیاتی", "path": "Workflow + Expert"},
    {"code": "S06", "title": "اظهارنامه", "path": "راهنما + نیمه‌خودکار"},
    {"code": "S07", "title": "سامانه مودیان", "path": "دانش + راهنما"},
    {"code": "S08", "title": "ارزش افزوده", "path": "RAG + Case"},
    {"code": "S09", "title": "جرائم مالیاتی", "path": "RAG + Risk"},
    {"code": "S10", "title": "بررسی قرارداد", "path": "Document AI"},
    {"code": "S11", "title": "محاسبات مالیاتی", "path": "ابزار + Expert"},
    {"code": "S12", "title": "ارزیابی ریسک مالیاتی", "path": "Risk Scoring"},
    {"code": "S13", "title": "ارجاع به مشاور متخصص", "path": "Marketplace"},
]

COMPLEX_KEYWORDS = (
    "برگ تشخیص",
    "هیئت",
    "لایحه",
    "اعتراض",
    "اجراییه",
    "توقیف",
    "دیوان",
    "کیفری",
    "فرار مالیاتی",
    "حسابرسی",
)
MEDIUM_KEYWORDS = (
    "اظهارنامه",
    "ارزش افزوده",
    "جریمه",
    "مودیان",
    "تبصره",
    "قسط",
    "بخشودگی",
    "قرارداد",
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _id(prefix: str) -> str:
    return f"{prefix}-{_now().strftime('%Y%m%d%H%M%S%f')[:-3]}"


def _append_jsonl(path: Path, rec: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")


def _read_jsonl(path: Path, limit: int = 50) -> list[dict]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    items: list[dict] = []
    for line in lines[-max(1, min(limit, 200)) :]:
        try:
            items.append(json.loads(line))
        except Exception:
            continue
    items.reverse()
    return items


def _title_for(code: str) -> str:
    for s in SERVICE_CATALOG:
        if s["code"] == code:
            return s["title"]
    return code


def triage_text(query: str, service_code: Optional[str] = None) -> dict[str, Any]:
    q = (query or "").strip()
    low = q.lower()
    # Persian keywords — check original
    if any(k in q for k in COMPLEX_KEYWORDS) or service_code in {
        "S03",
        "S04",
        "S05",
        "S13",
    }:
        level = "complex"
        reason = "کلیدواژه یا خدمت پیچیده — ارجاع مشاور / Human-in-the-loop"
        route = "expert"
        human = True
        rec = service_code or "S13"
    elif any(k in q for k in MEDIUM_KEYWORDS) or service_code in {
        "S02",
        "S06",
        "S08",
        "S09",
        "S10",
        "S11",
        "S12",
    }:
        level = "medium"
        reason = "نیاز به تحلیل عمیق‌تر یا کنترل کیفیت"
        route = "ai_quality_gate"
        human = True
        rec = service_code or "S02"
    else:
        level = "simple"
        reason = "سؤال عمومی — مسیر AI + RAG با Citation"
        route = "ai_rag"
        human = False
        rec = service_code or "S01"

    # Long unstructured text → bump complexity
    if len(q) > 800 and level == "simple":
        level = "medium"
        reason = "متن طولانی — کنترل کیفیت"
        route = "ai_quality_gate"
        human = True

    return {
        "level": level,
        "reason": reason,
        "recommended_service": rec,
        "route": route,
        "human_review_required": human,
    }


class TaxCaseCreate(BaseModel):
    taxpayer_name: str = Field(..., min_length=2, max_length=200)
    mobile: Optional[str] = Field(default=None, max_length=20)
    tax_year: Optional[int] = None
    province: Optional[str] = Field(default=None, max_length=80)
    city: Optional[str] = Field(default=None, max_length=80)
    summary: str = Field(..., min_length=5, max_length=4000)
    service_code: str = Field(default="S01", max_length=10)


class ServiceRequestCreate(BaseModel):
    service_code: str = Field(..., max_length=10)
    case_id: Optional[str] = None
    full_name: str = Field(..., min_length=2, max_length=200)
    mobile: str = Field(..., min_length=10, max_length=20)
    details: str = Field(..., min_length=5, max_length=4000)
    preferred_channel: str = Field(default="web", max_length=40)


class TriageIn(BaseModel):
    query: str = Field(..., min_length=3, max_length=4000)
    service_code: Optional[str] = None


class CaseNoteIn(BaseModel):
    note: str = Field(..., min_length=1, max_length=2000)


@router.get("/v1/services/catalog")
async def service_catalog():
    return {"items": SERVICE_CATALOG, "count": len(SERVICE_CATALOG)}


@router.post("/v1/triage")
async def triage(body: TriageIn):
    return triage_text(body.query, body.service_code)


@router.post("/v1/cases")
async def create_case(body: TaxCaseCreate):
    t = triage_text(body.summary, body.service_code)
    rec = {
        "id": _id("case"),
        "created_at": _now().isoformat(),
        "updated_at": _now().isoformat(),
        "status": "open",
        "triage": t["level"],
        "triage_reason": t["reason"],
        "route": t["route"],
        "taxpayer_name": body.taxpayer_name,
        "mobile": body.mobile,
        "tax_year": body.tax_year,
        "province": body.province,
        "city": body.city,
        "summary": body.summary,
        "service_code": body.service_code,
        "service_title": _title_for(body.service_code),
        "document_refs": [],
        "notes": [],
        "human_review_required": t["human_review_required"] or t["level"] != "simple",
    }
    _append_jsonl(CASE_STORE, rec)
    return {"ok": True, **rec}


@router.get("/v1/cases")
async def list_cases(limit: int = 50):
    items = _read_jsonl(CASE_STORE, limit=limit)
    return {"items": items, "count": len(items)}


@router.get("/v1/cases/{case_id}")
async def get_case(case_id: str):
    items = _read_jsonl(CASE_STORE, limit=200)
    for it in items:
        if it.get("id") == case_id:
            return it
    raise HTTPException(status_code=404, detail="case not found")


@router.post("/v1/cases/{case_id}/notes")
async def add_case_note(case_id: str, body: CaseNoteIn):
    """MVP: append a note event (full rewrite of case line not implemented)."""
    items = _read_jsonl(CASE_STORE, limit=200)
    found = None
    for it in items:
        if it.get("id") == case_id:
            found = it
            break
    if not found:
        raise HTTPException(status_code=404, detail="case not found")
    note_rec = {
        "id": _id("note"),
        "case_id": case_id,
        "created_at": _now().isoformat(),
        "note": body.note,
        "human_review_required": True,
    }
    note_store = ROOT / "data" / "tax_case_notes.jsonl"
    _append_jsonl(note_store, note_rec)
    return {"ok": True, **note_rec}


@router.post("/v1/services/requests")
async def create_service_request(body: ServiceRequestCreate):
    codes = {s["code"] for s in SERVICE_CATALOG}
    if body.service_code not in codes:
        raise HTTPException(status_code=400, detail="invalid service_code")
    t = triage_text(body.details, body.service_code)
    rec = {
        "id": _id("srv"),
        "created_at": _now().isoformat(),
        "status": "new",
        "service_code": body.service_code,
        "service_title": _title_for(body.service_code),
        "case_id": body.case_id,
        "full_name": body.full_name,
        "mobile": body.mobile,
        "details": body.details,
        "preferred_channel": body.preferred_channel,
        "triage": t["level"],
        "route": t["route"],
        "human_review_required": True,
    }
    _append_jsonl(SERVICE_STORE, rec)
    return {
        "ok": True,
        "message": "درخواست خدمت ثبت شد.",
        **rec,
    }


@router.get("/v1/services/requests")
async def list_service_requests(limit: int = 50):
    items = _read_jsonl(SERVICE_STORE, limit=limit)
    return {"items": items, "count": len(items)}
