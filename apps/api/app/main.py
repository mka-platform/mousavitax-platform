"""MousaviTax API Gateway – health + Tax Waiver + RAG chat (ADR-004)."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[3]
PACKAGES = ROOT / "packages"
for sub in (
    "shared",
    "ai-gateway/app",
    "taxlaw-engine",
    "prompt-engine",
    "knowledge-core",
    "embedding-service/app",
    "retrieval-engine/app",
    "document-parser",
):
    p = PACKAGES / sub
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

# Default vector DB relative to repo
os.environ.setdefault(
    "VECTOR_DB_PATH", str(ROOT / "data" / "iran_tax_vectors.json")
)
os.environ.setdefault("EMBEDDING_PROVIDER", "fallback")

app = FastAPI(
    title="MousaviTax API Gateway",
    version="0.3.1",
    description="MKA / ARYA – Iran Tax API (waiver + RAG)",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# ── Knowledge ───────────────────────────────────────────────
_ks: Any = None


def get_knowledge() -> Any:
    global _ks
    if _ks is not None:
        return _ks
    try:
        from knowledge_core import KnowledgeService  # type: ignore

        _ks = KnowledgeService(
            persist_path=os.environ.get(
                "VECTOR_DB_PATH", str(ROOT / "data" / "iran_tax_vectors.json")
            )
        )
    except Exception:
        _ks = None
    return _ks


# ── LLM (optional) ──────────────────────────────────────────
_gateway: Any = None


def get_gateway() -> Any:
    global _gateway
    if _gateway is not None:
        return _gateway
    try:
        from gateway import AIGateway  # type: ignore

        _gateway = AIGateway()
    except Exception:
        _gateway = None
    return _gateway


SYSTEM_TAX = """شما دستیار مشاور مالیاتی فارسی‌زبان MousaviTax هستید.
فقط بر اساس شواهد بازیابی‌شده پاسخ دهید. اگر شواهد کافی نیست بگویید.
در پایان منابع را به‌صورت فهرست ذکر کنید.
تصمیم نهایی با مشاور رسمی است؛ پیشنهاد شما جایگزین رأی سازمان نیست.
لحن رسمی، دقیق و مختصر باشد."""


@app.get("/health")
async def health():
    ks = get_knowledge()
    return {
        "status": "ok",
        "service": "mousavitax-api",
        "version": "0.3.1",
        "knowledge_chunks": ks.count() if ks else 0,
    }


# ── Tax Waiver (unchanged logic) ────────────────────────────
try:
    from taxlaw_engine import (
        CIRCULAR_CONFIG,
        DOC_CHECKLIST,
        DEFAULT_PENALTY_TYPES,
        PenaltyRow,
        WaiverInput,
        calculate_waiver,
        run_smoke_tests,
        WAIVER_VERSION,
    )
except ImportError:
    calculate_waiver = None  # type: ignore
    run_smoke_tests = None  # type: ignore
    CIRCULAR_CONFIG = {}  # type: ignore
    DOC_CHECKLIST = []  # type: ignore
    DEFAULT_PENALTY_TYPES = []  # type: ignore
    WAIVER_VERSION = "unavailable"


class PenaltyIn(BaseModel):
    type: str = "سایر"
    amount: float = 0
    waivable: bool = True


class WaiverCalcRequest(BaseModel):
    year: int = 1403
    appeal_stages: int = 0
    reduce_debt_30: bool = False
    after_executive_one_month: bool = False
    pay_type: str = "پرداخت نقدی"
    art190_80: bool = False
    art190_40: bool = False
    is_production_unit: bool = False
    special_ok: bool = True
    pay_date: str = ""
    penalties: list[PenaltyIn] = Field(default_factory=list)
    taxpayer_name: Optional[str] = None
    source: Optional[str] = None


@app.get("/v1/tax/waiver/meta")
async def waiver_meta():
    if calculate_waiver is None:
        raise HTTPException(status_code=503, detail="taxlaw-engine not installed")
    circ = CIRCULAR_CONFIG.get("circulars", {}).get(
        CIRCULAR_CONFIG.get("activeCircularId", ""), {}
    )
    return {
        "waiver_version": WAIVER_VERSION,
        "circular": circ,
        "penalty_types": list(DEFAULT_PENALTY_TYPES),
        "doc_checklist": list(DOC_CHECKLIST),
        "human_review_required": True,
    }


@app.post("/v1/tax/waiver/calculate")
async def waiver_calculate(body: WaiverCalcRequest):
    if calculate_waiver is None:
        raise HTTPException(status_code=503, detail="taxlaw-engine not installed")
    pay_type = (
        body.pay_type
        if body.pay_type in ("پرداخت نقدی", "ترتیب پرداخت")
        else "پرداخت نقدی"
    )
    inp = WaiverInput(
        year=body.year,
        appeal_stages=body.appeal_stages,
        reduce_debt_30=body.reduce_debt_30,
        after_executive_one_month=body.after_executive_one_month,
        pay_type=pay_type,  # type: ignore
        art190_80=body.art190_80,
        art190_40=body.art190_40,
        is_production_unit=body.is_production_unit,
        special_ok=body.special_ok,
        pay_date=body.pay_date or "",
        penalties=[
            PenaltyRow(type=p.type, amount=p.amount, waivable=p.waivable)
            for p in body.penalties
        ],
    )
    result = calculate_waiver(inp)
    out = result.to_dict() if hasattr(result, "to_dict") else result
    if isinstance(out, dict):
        out["taxpayer_name"] = body.taxpayer_name
        out["source"] = body.source
    return out


@app.get("/v1/tax/waiver/smoke")
async def waiver_smoke():
    if run_smoke_tests is None:
        raise HTTPException(status_code=503, detail="taxlaw-engine not installed")
    return {"tests": run_smoke_tests()}


# ── RAG / Chat ──────────────────────────────────────────────
class RAGRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=4000)
    top_k: int = Field(default=5, ge=1, le=15)


class CitationOut(BaseModel):
    source_id: str
    title: str
    score: float = 0.0
    page: Optional[int] = None
    snippet: str = ""


def _hits_to_citations(hits: list[dict]) -> list[dict]:
    out = []
    for h in hits:
        out.append(
            {
                "source_id": str(h.get("source_id") or h.get("chunk_id") or "unknown"),
                "title": str(h.get("title") or h.get("source_id") or "منبع"),
                "score": float(h.get("score") or 0),
                "page": h.get("page"),
                "snippet": (h.get("text") or "")[:280],
            }
        )
    return out


def _extractive_answer(query: str, hits: list[dict]) -> str:
    if not hits:
        return (
            "در دانش ایندکس‌شده موردی یافت نشد. "
            "لطفاً `python scripts/seed_knowledge.py` را اجرا کنید "
            "یا PDF رسمی را در knowledge/official قرار دهید. "
            "برای پرونده خاص با مشاور رسمی (۰۹۱۵۳۰۶۸۳۲۲) تماس بگیرید."
        )
    parts = [
        f"بر اساس {len(hits)} قطعه دانش بازیابی‌شده (پاسخ استخراجی — بدون LLM):",
        "",
    ]
    for i, h in enumerate(hits[:5], 1):
        title = h.get("title") or h.get("source_id") or "منبع"
        text = (h.get("text") or "").strip().replace("\n", " ")
        parts.append(f"{i}. [{title}] {text[:420]}")
        parts.append("")
    parts.append(
        "— این خلاصه خودکار است و نیاز به بررسی مشاور دارد. "
        "HUMAN_REVIEW_REQUIRED · ۰۹۱۵۳۰۶۸۳۲۲"
    )
    return "\n".join(parts)


@app.get("/v1/knowledge/status")
async def knowledge_status():
    ks = get_knowledge()
    path = os.environ.get("VECTOR_DB_PATH", "")
    return {
        "ready": ks is not None and ks.count() > 0,
        "chunks": ks.count() if ks else 0,
        "vector_db_path": path,
        "embedding_provider": os.getenv("EMBEDDING_PROVIDER", "fallback"),
    }


@app.post("/v1/rag/query")
async def rag_query(body: RAGRequest):
    ks = get_knowledge()
    hits: list[dict] = []
    if ks is not None:
        try:
            hits = ks.query(body.query, top_k=body.top_k) or []
        except Exception:
            hits = []

    citations = _hits_to_citations(hits)
    model_name = "extractive"
    latency_ms = 0
    answer = _extractive_answer(body.query, hits)

    gw = get_gateway()
    provider = os.getenv("LLM_PROVIDER", "").lower()
    # فقط اگر LLM پیکربندی شده و hit داریم تلاش کن
    if gw is not None and hits and provider in ("ollama", "openai", "openrouter", "gemini"):
        ctx = "\n\n".join(
            f"[{i}] {h.get('title', '')}\n{(h.get('text') or '')[:900]}"
            for i, h in enumerate(hits, 1)
        )
        user = f"شواهد:\n{ctx}\n\nپرسش کاربر:\n{body.query}"
        try:
            text, model_name, latency_ms = await gw.generate(
                SYSTEM_TAX, user, temperature=0.25, max_tokens=1200
            )
            answer = text
        except Exception as e:
            answer = (
                _extractive_answer(body.query, hits)
                + f"\n\n(توجه: LLM در دسترس نبود — {type(e).__name__})"
            )
            model_name = "extractive-fallback"

    if not citations:
        citations = [
            {
                "source_id": "pending-index",
                "title": "دانش ایندکس‌نشده — seed_knowledge را اجرا کنید",
                "score": 0.0,
                "page": None,
                "snippet": "",
            }
        ]

    return {
        "answer": answer,
        "citations": citations,
        "model": model_name,
        "latency_ms": latency_ms,
        "human_review_required": True,
    }




# ── Advisor marketplace requests ─────────────────────────────
ADVISOR_STORE = ROOT / "data" / "advisor_requests.jsonl"


class AdvisorRequestIn(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    mobile: str = Field(..., min_length=10, max_length=20)
    city: str = Field(default="", max_length=80)
    topic: str = Field(..., min_length=2, max_length=200)
    details: str = Field(default="", max_length=4000)
    preferred_time: str = Field(default="", max_length=120)
    role: str = Field(default="مودی", max_length=40)  # مودی | مشاور


@app.post("/v1/advisors/request")
async def advisor_request(body: AdvisorRequestIn):
    import json
    from datetime import datetime, timezone

    ADVISOR_STORE.parent.mkdir(parents=True, exist_ok=True)
    rec = {
        "id": f"adv-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "new",
        "human_review_required": True,
        **body.model_dump(),
    }
    with ADVISOR_STORE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return {
        "ok": True,
        "id": rec["id"],
        "message": "درخواست ثبت شد. مشاور انسانی به‌زودی بررسی می‌کند.",
        "contact_hint": "۰۹۱۵۳۰۶۸۳۲۲",
    }


@app.get("/v1/advisors/requests")
async def list_advisor_requests(limit: int = 50):
    """MVP: لیست خام برای مدیر — بعداً با احراز هویت محدود شود."""
    import json

    if not ADVISOR_STORE.exists():
        return {"items": [], "count": 0}
    lines = ADVISOR_STORE.read_text(encoding="utf-8").strip().splitlines()
    items = []
    for line in lines[-max(1, min(limit, 200)) :]:
        try:
            items.append(json.loads(line))
        except Exception:
            continue
    items.reverse()
    return {"items": items, "count": len(items)}


@app.get("/")
async def root():
    ks = get_knowledge()
    return {
        "service": "MousaviTax API Gateway",
        "version": "0.3.1",
        "health": "/health",
        "docs": "/docs",
        "knowledge_status": "/v1/knowledge/status",
        "rag": "POST /v1/rag/query",
        "waiver_calculate": "POST /v1/tax/waiver/calculate",
        "advisor_request": "POST /v1/advisors/request",
        "knowledge_chunks": ks.count() if ks else 0,
        "note": "Web UI on Next.js :3000",
    }
