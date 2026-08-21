"""MousaviTax API Gateway – RAG + APCS + Knowledge retrieval."""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
load_dotenv()

# Default vector path relative to repo
os.environ.setdefault(
    "VECTOR_DB_PATH", str(ROOT / "data" / "iran_tax_vectors.json")
)

PACKAGES = ROOT / "packages"
for sub in (
    "shared",
    "ai-gateway/app",
    "prompt-engine",
    "knowledge-core",
    "embedding-service/app",
    "retrieval-engine/app",
    "taxlaw-engine",
):
    sys.path.insert(0, str(PACKAGES / sub))

from mousavitax_shared.models import (  # noqa: E402
    Citation,
    HealthResponse,
    RAGRequest,
    RAGResponse,
    SourceType,
)
from gateway import AIGateway, AIGatewayError  # noqa: E402

try:
    from prompt_engine import (  # noqa: E402
        APCSParser,
        APCSValidator,
        PromptBuilder,
        QualityGate,
    )
except ImportError:
    APCSParser = PromptBuilder = APCSValidator = QualityGate = None  # type: ignore

try:
    from knowledge_core import KnowledgeService  # noqa: E402
except ImportError:
    KnowledgeService = None  # type: ignore

app = FastAPI(
    title="MousaviTax API Gateway",
    description="MKA/ARYA Holding – Iran Tax · APCS + Retrieval",
    version="0.6.0",
    contact={"email": "ziya.mka2026@gmail.com"},
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gateway = AIGateway()
_knowledge: Any = None


def get_knowledge() -> Any:
    global _knowledge
    if _knowledge is None and KnowledgeService is not None:
        try:
            _knowledge = KnowledgeService()
        except Exception:
            _knowledge = None
    return _knowledge


class APCSQueryRequest(BaseModel):
    apcs: Optional[str] = None
    query: Optional[str] = Field(default=None, max_length=4000)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    top_k: int = Field(default=5, ge=1, le=20)
    domain: str = "iran-tax"
    skip_retrieval: bool = False


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(version="0.6.0")


@app.get("/v1/knowledge/status")
async def knowledge_status():
    ks = get_knowledge()
    return {
        "available": ks is not None,
        "chunks": ks.count() if ks else 0,
        "vector_db_path": os.environ.get("VECTOR_DB_PATH"),
        "embedding_provider": os.environ.get("EMBEDDING_PROVIDER", "ollama"),
    }


def _hits_to_citations(hits: list[dict]) -> list[Citation]:
    out: list[Citation] = []
    for h in hits:
        try:
            st = h.get("source_type") or "manual"
            try:
                source_type = SourceType(st)
            except Exception:
                source_type = SourceType.MANUAL
            out.append(
                Citation(
                    source_id=str(h.get("source_id") or "unknown"),
                    source_type=source_type,
                    title=str(h.get("title") or "بدون عنوان"),
                    chunk_id=str(h.get("chunk_id") or ""),
                    score=float(min(max(h.get("score") or 0.0, 0.0), 1.0)),
                    page=h.get("page"),
                    section=h.get("section"),
                    url=h.get("url"),
                )
            )
        except Exception:
            continue
    return out


@app.post("/v1/rag/query", response_model=RAGResponse)
async def rag_query(request: RAGRequest):
    wrapped = APCSQueryRequest(
        query=request.query,
        user_id=request.user_id,
        session_id=request.session_id,
        top_k=request.top_k,
    )
    return await apcs_query(wrapped)


@app.post("/v1/apcs/query", response_model=RAGResponse)
async def apcs_query(request: APCSQueryRequest):
    if not request.query and not request.apcs:
        raise HTTPException(status_code=400, detail="query or apcs required")

    try:
        cmd = None
        if APCSParser and request.apcs:
            cmd = APCSParser().parse(request.apcs)
            if APCSValidator:
                vr = APCSValidator().validate(cmd)
                if not vr.ok:
                    raise HTTPException(status_code=400, detail={"apcs_errors": vr.errors})

        hits: list[dict] = []
        qtext = request.query or (cmd.task if cmd else None) or ""
        ks = get_knowledge()
        if ks and qtext and not request.skip_retrieval:
            hits = ks.query(qtext, top_k=request.top_k)

        if cmd and PromptBuilder:
            built = PromptBuilder(domain=request.domain).build(
                cmd, retrieved_context=hits, user_message=request.query
            )
            system, user = built["system"], built["user"]
        else:
            sys_path = ROOT / "domains" / request.domain / "prompts" / "advisor_system.txt"
            system = (
                sys_path.read_text(encoding="utf-8")
                if sys_path.exists()
                else "You are a careful Persian tax assistant. Do not fabricate sources."
            )
            if hits:
                ctx = "\n\n".join(
                    f"[{i}] {h.get('title', '')}\n{h.get('text', '')[:800]}"
                    for i, h in enumerate(hits, 1)
                )
                user = f"شواهد:\n{ctx}\n\nپرسش:\n{request.query}"
            else:
                user = request.query or request.apcs or ""

        answer, model_name, latency_ms = await gateway.generate(
            system_prompt=system,
            user_prompt=user,
            temperature=0.3,
            max_tokens=1600,
        )

        if cmd and QualityGate and (cmd.quality_gate or cmd.verify):
            gate = QualityGate().evaluate(cmd, answer, retrieved=hits)
            if not gate.passed and gate.status:
                answer = f"{gate.status}\n\n" + "\n".join(gate.reasons) + f"\n\n---\n{answer}"

        citations = _hits_to_citations(hits)
        if not citations:
            citations = [
                Citation(
                    source_id="pending-index",
                    source_type=SourceType.MANUAL,
                    title="دانش ایندکس‌نشده یا بدون hit — ابتدا scripts/seed_knowledge.py را اجرا کنید",
                    chunk_id="gen-001",
                    score=0.0,
                    section="موقت",
                )
            ]

        return RAGResponse(
            answer=answer,
            citations=citations,
            model=model_name,
            latency_ms=latency_ms,
            request_id=f"req-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        )
    except HTTPException:
        raise
    except AIGatewayError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")




# ─── Tax Waiver Engine ───────────────────────────────────────
try:
    from taxlaw_engine import (  # noqa: E402
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
    pay_type = body.pay_type if body.pay_type in ("پرداخت نقدی", "ترتیب پرداخت") else "پرداخت نقدی"
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
    out = result.to_dict()
    out["taxpayer_name"] = body.taxpayer_name
    out["source"] = body.source
    return out


@app.get("/v1/tax/waiver/smoke")
async def waiver_smoke():
    if run_smoke_tests is None:
        raise HTTPException(status_code=503, detail="taxlaw-engine not installed")
    return {"tests": run_smoke_tests()}

@app.get("/")
async def root():
    ks = get_knowledge()
    return {
        "service": "MousaviTax API Gateway",
        "holding": "MKA / ARYA",
        "domain": "iran-tax",
        "apcs": "v1.0",
        "version": "0.6.0",
        "knowledge_chunks": ks.count() if ks else 0,
        "docs": "/docs",
        "rag": "/v1/rag/query",
        "apcs_query": "/v1/apcs/query",
        "knowledge_status": "/v1/knowledge/status",
        "waiver_calculate": "/v1/tax/waiver/calculate",
        "waiver_meta": "/v1/tax/waiver/meta",
        "llm_provider": gateway.provider,
    }
