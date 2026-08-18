"""MousaviTax / MKA Backend API – API Gateway."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
load_dotenv()

# Monorepo imports
PACKAGES = ROOT / "packages"
sys.path.insert(0, str(PACKAGES / "shared"))
sys.path.insert(0, str(PACKAGES / "ai-gateway" / "app"))

from mousavitax_shared.models import (  # noqa: E402
    Citation,
    HealthResponse,
    RAGRequest,
    RAGResponse,
    SourceType,
)
from gateway import AIGateway, AIGatewayError  # noqa: E402

DOMAIN_PROMPT = (
    ROOT / "domains" / "iran-tax" / "prompts" / "advisor_system.txt"
).read_text(encoding="utf-8")

app = FastAPI(
    title="MousaviTax API Gateway",
    description="MKA Holding – Iran Tax vertical public API",
    version="0.3.0",
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


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(version="0.3.0")


@app.post("/v1/rag/query", response_model=RAGResponse)
async def rag_query(request: RAGRequest):
    """RAG endpoint. Retrieval connects when knowledge index is populated."""
    try:
        user_prompt = f"پرسش کاربر:\n{request.query}"
        answer, model_name, latency_ms = await gateway.generate(
            system_prompt=DOMAIN_PROMPT,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=1200,
        )
        citations = [
            Citation(
                source_id="pending-index",
                source_type=SourceType.MANUAL,
                title="پایگاه دانش رسمی هنوز کامل ایندکس نشده — پاسخ بر اساس مدل",
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
        "holding": "MKA",
        "domain": "iran-tax",
        "version": "0.3.0",
        "docs": "/docs",
        "health": "/health",
        "rag": "/v1/rag/query",
        "llm_provider": gateway.provider,
    }
