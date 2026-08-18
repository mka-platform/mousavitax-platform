"""MousaviTax / MKA Backend API – API Gateway + APCS-aware RAG."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
load_dotenv()

PACKAGES = ROOT / "packages"
sys.path.insert(0, str(PACKAGES / "shared"))
sys.path.insert(0, str(PACKAGES / "ai-gateway" / "app"))
sys.path.insert(0, str(PACKAGES / "prompt-engine"))

from mousavitax_shared.models import (  # noqa: E402
    Citation,
    HealthResponse,
    RAGRequest,
    RAGResponse,
    SourceType,
)
from gateway import AIGateway, AIGatewayError  # noqa: E402

try:
    from prompt_engine import APCSParser, PromptBuilder  # noqa: E402
except ImportError:
    APCSParser = None  # type: ignore
    PromptBuilder = None  # type: ignore

app = FastAPI(
    title="MousaviTax API Gateway",
    description="MKA Holding – Iran Tax vertical · APCS-aware public API",
    version="0.4.0",
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


class APCSQueryRequest(BaseModel):
    """Optional full APCS command text; falls back to simple RAG query."""

    apcs: Optional[str] = Field(
        default=None, description="Raw APCS command block"
    )
    query: Optional[str] = Field(default=None, min_length=1, max_length=4000)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    top_k: int = Field(default=5, ge=1, le=20)
    domain: str = "iran-tax"


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(version="0.4.0")


def _build_prompts(req: APCSQueryRequest) -> tuple[str, str]:
    if APCSParser and PromptBuilder and req.apcs:
        cmd = APCSParser().parse(req.apcs)
        built = PromptBuilder(domain=req.domain).build(
            cmd, user_message=req.query
        )
        return built["system"], built["user"]

    # Fallback: domain system prompt + user query
    sys_path = ROOT / "domains" / req.domain / "prompts" / "advisor_system.txt"
    system = (
        sys_path.read_text(encoding="utf-8")
        if sys_path.exists()
        else "You are a careful Persian tax assistant. Do not fabricate sources."
    )
    user = req.query or (req.apcs or "")
    return system, user


@app.post("/v1/rag/query", response_model=RAGResponse)
async def rag_query(request: RAGRequest):
    """Simple RAG-style query (backward compatible)."""
    wrapped = APCSQueryRequest(query=request.query, user_id=request.user_id, session_id=request.session_id, top_k=request.top_k)
    return await apcs_query(wrapped)


@app.post("/v1/apcs/query", response_model=RAGResponse)
async def apcs_query(request: APCSQueryRequest):
    """APCS-aware endpoint: parse commands, build prompt, call model."""
    if not request.query and not request.apcs:
        raise HTTPException(status_code=400, detail="query or apcs required")
    try:
        system, user = _build_prompts(request)
        answer, model_name, latency_ms = await gateway.generate(
            system_prompt=system,
            user_prompt=user,
            temperature=0.3,
            max_tokens=1600,
        )
        citations = [
            Citation(
                source_id="pending-index",
                source_type=SourceType.MANUAL,
                title="پایگاه دانش رسمی هنوز کامل ایندکس نشده — پاسخ بر اساس مدل + APCS",
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
    except AIGatewayError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


@app.get("/")
async def root():
    return {
        "service": "MousaviTax API Gateway",
        "holding": "MKA / ARYA",
        "domain": "iran-tax",
        "apcs": "v1.0",
        "version": "0.4.0",
        "docs": "/docs",
        "health": "/health",
        "rag": "/v1/rag/query",
        "apcs_query": "/v1/apcs/query",
        "llm_provider": gateway.provider,
    }
