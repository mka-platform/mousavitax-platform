"""Tax Waiver calculator – port of TAXLAW-WAIVER-CALCULATOR v1.3.0 (Apps Script)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

WAIVER_VERSION = "1.3.0-py"

CIRCULAR_CONFIG: dict[str, Any] = {
    "activeCircularId": "200-1404-504",
    "circulars": {
        "200-1404-504": {
            "id": "200/1404/504",
            "title": "تفویض اختیار بخشودگی جرائم قابل بخشش",
            "date": "1404/07/21",
            "effectiveFrom": "1404/09/01",
            "baseRates": {
                "1403+": 1.00,
                "1402": 0.95,
                "1401": 0.85,
                "1400": 0.75,
                "1399-": 0.65,
            },
            "deductions": {"perAppealStage": 0.05, "afterExecutiveOneMonth": 0.10},
            "floors": {"cash": 0.30, "installment": 0.20},
        }
    },
    "specialIncreases": [
        {
            "id": "200-14064-d",
            "title": "افزایش تفویض واحدهای تولیدی و آسیب‌دیده از جنگ رمضان",
            "date": "1405/05/25",
            "bands": [
                {"from": "1405/05/26", "to": "1405/05/31", "rate": 0.20},
                {"from": "1405/06/01", "to": "1405/06/15", "rate": 0.15},
                {"from": "1405/06/16", "to": "1405/06/31", "rate": 0.10},
            ],
        }
    ],
    "art190": {
        "exemptionAcceptOrAgreement": 0.80,
        "exemptionWithinOneMonthFinal": 0.40,
    },
}

DEFAULT_PENALTY_TYPES = [
    "جریمه تأخیر ماده ۱۹۰",
    "جریمه ماده ۱۹۲",
    "جریمه ماده ۱۶۹",
    "جریمه بند ب ماده ۳۶ ارزش افزوده",
    "جریمه ماده ۳۷ ارزش افزوده",
    "جریمه حقوق",
    "جریمه اجاره/نقل‌وانتقال",
    "سایر قابل بخشش",
    "جرائم غیرقابل بخشش",
    "سایر",
]

DOC_CHECKLIST = [
    "برگ تشخیص (ابلاغ‌شده)",
    "برگ قطعی",
    "رسید پرداخت یا ترتیب پرداخت",
    "اظهارنامه تسلیمی",
    "مدارک تکالیف قانونی (دفاتر/اسناد)",
    "توافق ماده ۲۳۹ یا قبولی تشخیص",
    "مدارک واحد تولیدی",
    "مدارک آسیب‌دیدگی جنگ رمضان",
    "آرای مراحل دادرسی",
    "مدارک کاهش بدهی ≥۳۰٪",
    "برگ اجرایی و تاریخ ابلاغ",
    "خسارت تأخیر ماده ۲۴۲",
    "لیست جرائم غیرقابل بخشش",
    "وکالتنامه نماینده",
]


@dataclass
class PenaltyRow:
    type: str
    amount: float
    waivable: bool = True


@dataclass
class WaiverInput:
    year: int = 1403
    appeal_stages: int = 0
    reduce_debt_30: bool = False
    after_executive_one_month: bool = False
    pay_type: Literal["پرداخت نقدی", "ترتیب پرداخت"] = "پرداخت نقدی"
    art190_80: bool = False
    art190_40: bool = False
    is_production_unit: bool = False
    special_ok: bool = True
    pay_date: str = ""
    penalties: list[PenaltyRow] = field(default_factory=list)


@dataclass
class WaiverResult:
    rule_version: str
    circular_id: str
    base_after_deductions: float
    art190_rate: float
    special_add: float
    final_pct: float
    waivable_sum: float
    non_waivable_sum: float
    waived_amount: float
    remaining: float
    human_review_required: bool
    disclaimer: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_version": self.rule_version,
            "circular_id": self.circular_id,
            "base_after_deductions": self.base_after_deductions,
            "art190_rate": self.art190_rate,
            "special_add": self.special_add,
            "final_pct": self.final_pct,
            "waivable_sum": self.waivable_sum,
            "non_waivable_sum": self.non_waivable_sum,
            "waived_amount": self.waived_amount,
            "remaining": self.remaining,
            "human_review_required": self.human_review_required,
            "disclaimer": self.disclaimer,
        }


def _base_rate(year: int) -> float:
    circ = CIRCULAR_CONFIG["circulars"][CIRCULAR_CONFIG["activeCircularId"]]
    rates = circ["baseRates"]
    if year >= 1403:
        return rates["1403+"]
    if year == 1402:
        return rates["1402"]
    if year == 1401:
        return rates["1401"]
    if year == 1400:
        return rates["1400"]
    return rates["1399-"]


def calculate_waiver(inp: WaiverInput) -> WaiverResult:
    circ = CIRCULAR_CONFIG["circulars"][CIRCULAR_CONFIG["activeCircularId"]]
    base = _base_rate(inp.year)
    ded_appeal = 0.0 if inp.reduce_debt_30 else inp.appeal_stages * circ["deductions"]["perAppealStage"]
    ded_exec = circ["deductions"]["afterExecutiveOneMonth"] if inp.after_executive_one_month else 0.0
    floor = circ["floors"]["cash"] if inp.pay_type == "پرداخت نقدی" else circ["floors"]["installment"]
    after_ded = max(floor, base - ded_appeal - ded_exec)

    art190 = (
        CIRCULAR_CONFIG["art190"]["exemptionAcceptOrAgreement"]
        if inp.art190_80
        else (
            CIRCULAR_CONFIG["art190"]["exemptionWithinOneMonthFinal"]
            if inp.art190_40
            else 0.0
        )
    )
    after_art = max(after_ded, art190)

    special_add = 0.0
    if inp.is_production_unit and inp.special_ok and inp.pay_date:
        for si in CIRCULAR_CONFIG["specialIncreases"]:
            for b in si["bands"]:
                if b["from"] <= inp.pay_date <= b["to"]:
                    special_add = max(special_add, b["rate"])

    final_pct = min(1.0, after_art + special_add)

    waivable = sum(max(0.0, p.amount) for p in inp.penalties if p.waivable)
    non_waivable = sum(max(0.0, p.amount) for p in inp.penalties if not p.waivable)
    waived = round(waivable * final_pct)
    remaining = waivable + non_waivable - waived

    return WaiverResult(
        rule_version=WAIVER_VERSION,
        circular_id=circ["id"],
        base_after_deductions=after_ded,
        art190_rate=art190,
        special_add=special_add,
        final_pct=final_pct,
        waivable_sum=waivable,
        non_waivable_sum=non_waivable,
        waived_amount=waived,
        remaining=remaining,
        human_review_required=True,
        disclaimer=(
            "خروجی سیستمی برای بررسی انسان است و جایگزین رأی سازمان امور مالیاتی "
            "یا مشاور رسمی نیست. HUMAN_REVIEW_REQUIRED"
        ),
    )


def run_smoke_tests() -> list[dict[str, Any]]:
    p = [PenaltyRow("جریمه تأخیر ماده ۱۹۰", 10_000_000, True)]
    r1 = calculate_waiver(WaiverInput(year=1403, penalties=p))
    r2 = calculate_waiver(WaiverInput(year=1403, appeal_stages=2, penalties=p))
    r3 = calculate_waiver(WaiverInput(year=1402, art190_80=True, penalties=p))
    return [
        {"name": "1403 نقدی بدون دادرسی → 100%", "ok": abs(r1.final_pct - 1.0) < 1e-9, "detail": r1.final_pct},
        {"name": "1403 با ۲ مرحله → 90%", "ok": abs(r2.final_pct - 0.9) < 1e-9, "detail": r2.final_pct},
        {"name": "1402 + ماده190-80 → 95%", "ok": abs(r3.final_pct - 0.95) < 1e-9, "detail": r3.final_pct},
    ]
