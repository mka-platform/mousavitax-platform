"""Tax Case + Service Request models (ADR-007 / docs/11_TAX_CASE)."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class CaseStatus(str, Enum):
    OPEN = "open"
    IN_REVIEW = "in_review"
    WAITING_CLIENT = "waiting_client"
    WAITING_EXPERT = "waiting_expert"
    RESOLVED = "resolved"
    ARCHIVED = "archived"


class TriageLevel(str, Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


class ServiceCode(str, Enum):
    S01 = "S01"  # سؤال سریع
    S02 = "S02"  # تحلیل پرونده
    S03 = "S03"  # برگ تشخیص
    S04 = "S04"  # لایحه
    S05 = "S05"  # اعتراض
    S06 = "S06"  # اظهارنامه
    S07 = "S07"  # سامانه مودیان
    S08 = "S08"  # ارزش افزوده
    S09 = "S09"  # جرائم
    S10 = "S10"  # قرارداد
    S11 = "S11"  # محاسبات
    S12 = "S12"  # ریسک
    S13 = "S13"  # ارجاع مشاور


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


class TaxCaseCreate(BaseModel):
    taxpayer_name: str = Field(..., min_length=2, max_length=200)
    mobile: Optional[str] = Field(default=None, max_length=20)
    national_id_hint: Optional[str] = Field(
        default=None, max_length=20, description="اختیاری؛ ترجیحاً کامل ذخیره نشود در MVP"
    )
    tax_year: Optional[int] = None
    province: Optional[str] = Field(default=None, max_length=80)
    city: Optional[str] = Field(default=None, max_length=80)
    summary: str = Field(..., min_length=5, max_length=4000)
    service_code: str = Field(default="S01", max_length=10)


class TaxCase(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    status: CaseStatus = CaseStatus.OPEN
    triage: TriageLevel = TriageLevel.SIMPLE
    taxpayer_name: str
    mobile: Optional[str] = None
    tax_year: Optional[int] = None
    province: Optional[str] = None
    city: Optional[str] = None
    summary: str
    service_code: str = "S01"
    document_refs: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    human_review_required: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class ServiceRequestCreate(BaseModel):
    service_code: str = Field(..., max_length=10)
    case_id: Optional[str] = None
    full_name: str = Field(..., min_length=2, max_length=200)
    mobile: str = Field(..., min_length=10, max_length=20)
    details: str = Field(..., min_length=5, max_length=4000)
    preferred_channel: str = Field(default="web", max_length=40)


class ServiceRequest(BaseModel):
    id: str
    created_at: datetime
    status: str = "new"
    service_code: str
    service_title: str = ""
    case_id: Optional[str] = None
    full_name: str
    mobile: str
    details: str
    preferred_channel: str = "web"
    triage: TriageLevel = TriageLevel.SIMPLE
    human_review_required: bool = True


class TriageRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=4000)
    service_code: Optional[str] = None


class TriageResponse(BaseModel):
    level: TriageLevel
    reason: str
    recommended_service: str
    route: str
    human_review_required: bool
