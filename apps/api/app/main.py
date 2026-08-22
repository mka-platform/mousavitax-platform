"""MousaviTax API Gateway – health + Tax Waiver (ADR-004).

Web (Next.js) runs separately on port 3000 and calls this API via NEXT_PUBLIC_API_URL.
Do NOT serve Next.js static files from this process.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[3]  # repo root when apps/api/app/main.py
PACKAGES = ROOT / "packages"
for sub in (
    "shared",
    "ai-gateway/app",
    "taxlaw-engine",
    "prompt-engine",
    "knowledge-core",
):
    p = PACKAGES / sub
    if p.exists():
        sys.path.insert(0, str(p))

app = FastAPI(
    title="MousaviTax API Gateway",
    version="0.2.3",
    description="MKA / ARYA – Iran Tax API (waiver + RAG stubs)",
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


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "mousavitax-api",
        "version": "0.2.3",
    }


# ─── Tax Waiver ─────────────────────────────────────────────
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
        raise HTTPException(status_code=503, detail="taxlaw-engine not installed on PYTHONPATH")
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
        raise HTTPException(status_code=503, detail="taxlaw-engine not installed on PYTHONPATH")
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


@app.get("/")
async def root():
    return {
        "service": "MousaviTax API Gateway",
        "version": "0.2.3",
        "health": "/health",
        "docs": "/docs",
        "waiver_meta": "/v1/tax/waiver/meta",
        "waiver_calculate": "POST /v1/tax/waiver/calculate",
        "note": "Web UI runs on Next.js :3000 — not served by this API",
    }
