"""MousaviTax API Gateway – RAG + APCS + Knowledge retrieval."""

from __future__ import annotations

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

PACKAGES = ROOT / "packages"
for sub in (
    "shared",
    "ai-gateway/app",
    "prompt-engine",
    "knowledge-core",
    "embedding-service/app",
    "retrieval-engine/app",
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
    version="0.5.0",
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
    ks = get_knowledge()
    extra = {"knowledge_chunks": ks.count() if ks else 0}
    h = HealthResponse(version="0.5.0")
    return h


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
                    score=float(h.get("score") or 0.0),
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

        # Retrieval
        hits: list[dict] = []
        qtext = request.query or (cmd.task if cmd else None) or ""
        ks = get_knowledge()
        if ks and qtext and not request.skip_retrieval:
            hits = ks.query(qtext, top_k=request.top_k)

        # Prompt build
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
                    title="دانش رسمی ایندکس‌نشده یا بدون hit — از ادعای قطعی قانونی خودداری شود",
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


@app.get("/")
async def root():
    ks = get_knowledge()
    return {
        "service": "MousaviTax API Gateway",
        "holding": "MKA / ARYA",
        "domain": "iran-tax",
        "apcs": "v1.0",
        "version": "0.5.0",
        "knowledge_chunks": ks.count() if ks else 0,
        "docs": "/docs",
        "rag": "/v1/rag/query",
        "apcs_query": "/v1/apcs/query",
        "llm_provider": gateway.provider,
    }
