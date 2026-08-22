"use client";

import { useMemo, useState } from "react";
import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const PENALTY_TYPES = [
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
];

type Penalty = { type: string; amount: number; waivable: boolean };

export default function WaiverPage() {
  const [year, setYear] = useState(1403);
  const [stages, setStages] = useState(0);
  const [reduce30, setReduce30] = useState(false);
  const [afterExec, setAfterExec] = useState(false);
  const [payType, setPayType] = useState("پرداخت نقدی");
  const [art80, setArt80] = useState(false);
  const [art40, setArt40] = useState(false);
  const [isProd, setIsProd] = useState(false);
  const [specialOk, setSpecialOk] = useState(true);
  const [payDate, setPayDate] = useState("");
  const [name, setName] = useState("");
  const [source, setSource] = useState("عملکرد");
  const [penalties, setPenalties] = useState<Penalty[]>(
    PENALTY_TYPES.map((t, i) => ({ type: t, amount: 0, waivable: i !== 8 })),
  );
  const [result, setResult] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onCalc = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API}/v1/tax/waiver/calculate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          year,
          appeal_stages: stages,
          reduce_debt_30: reduce30,
          after_executive_one_month: afterExec,
          pay_type: payType,
          art190_80: art80,
          art190_40: art40,
          is_production_unit: isProd,
          special_ok: specialOk,
          pay_date: payDate,
          penalties,
          taxpayer_name: name,
          source,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      setResult(await res.json());
    } catch (e) {
      setError(String(e));
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const pct = (n: unknown) =>
    typeof n === "number" ? `${(n * 100).toFixed(2)}٪` : "—";
  const num = (n: unknown) =>
    typeof n === "number" ? Math.round(n).toLocaleString("fa-IR") : "—";

  const boolRow = (
    label: string,
    val: boolean,
    set: (v: boolean) => void,
  ) => (
    <label className="flex items-center justify-between gap-2 rounded-lg border border-slate-700 p-3 text-sm">
      <span>{label}</span>
      <select
        className="rounded bg-slate-900 px-2 py-1"
        value={val ? "بله" : "خیر"}
        onChange={(e) => set(e.target.value === "بله")}
      >
        <option>خیر</option>
        <option>بله</option>
      </select>
    </label>
  );

  return (
    <main className="mx-auto max-w-3xl space-y-6 px-4 py-10 text-slate-100" dir="rtl">
      <div className="space-y-2">
        <p className="text-xs font-medium text-blue-400">ابزار عملیاتی · دستورالعمل ۲۰۰/۱۴۰۴/۵۰۴</p>
        <div className="flex items-center justify-between gap-4">
          <h1 className="text-2xl font-extrabold md:text-3xl">محاسبه‌گر بخشودگی جرائم</h1>
          <Link href="/" className="text-sm text-slate-400 hover:text-blue-400">
            خانه
          </Link>
        </div>
        <p className="text-sm leading-7 text-slate-400">
          پیشنهاد سیستمی برای بررسی مشاور — با درصد پایه، کسور دادرسی، ماده ۱۹۰ و افزایش ویژه.
        </p>
      </div>
      <div className="rounded-xl border border-amber-500/40 bg-amber-500/10 p-4 text-sm leading-7 text-amber-100">
        <strong>HUMAN_REVIEW_REQUIRED</strong> — این محاسبه جایگزین رأی سازمان امور مالیاتی
        یا مشاور رسمی نیست و باید توسط انسان تأیید شود.
      </div>

      <section className="space-y-3 rounded-2xl border border-slate-700 bg-[var(--card)] p-5">
        <h2 className="font-semibold">مشخصات</h2>
        <input
          className="w-full rounded border border-slate-600 bg-slate-900 px-3 py-2"
          placeholder="نام مودی"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <div className="grid gap-3 sm:grid-cols-2">
          <input
            type="number"
            className="rounded border border-slate-600 bg-slate-900 px-3 py-2"
            value={year}
            onChange={(e) => setYear(Number(e.target.value) || 1403)}
            placeholder="سال"
          />
          <select
            className="rounded border border-slate-600 bg-slate-900 px-3 py-2"
            value={source}
            onChange={(e) => setSource(e.target.value)}
          >
            {["عملکرد", "ارزش افزوده", "حقوق", "اجاره", "سایر"].map((s) => (
              <option key={s}>{s}</option>
            ))}
          </select>
          <input
            className="rounded border border-slate-600 bg-slate-900 px-3 py-2"
            placeholder="تاریخ پرداخت ۱۴۰۵/۰۵/۲۸"
            value={payDate}
            onChange={(e) => setPayDate(e.target.value)}
          />
          <input
            type="number"
            className="rounded border border-slate-600 bg-slate-900 px-3 py-2"
            value={stages}
            onChange={(e) => setStages(Number(e.target.value) || 0)}
            placeholder="مراحل دادرسی"
          />
        </div>
        <select
          className="w-full rounded border border-slate-600 bg-slate-900 px-3 py-2"
          value={payType}
          onChange={(e) => setPayType(e.target.value)}
        >
          <option>پرداخت نقدی</option>
          <option>ترتیب پرداخت</option>
        </select>
        <div className="grid gap-2 sm:grid-cols-2">
          {boolRow("کاهش بدهی ≥۳۰٪", reduce30, setReduce30)}
          {boolRow("پس از ۱ ماه اجرایی", afterExec, setAfterExec)}
          {boolRow("معافیت ۸۰٪ ماده ۱۹۰", art80, setArt80)}
          {boolRow("معافیت ۴۰٪ ماده ۱۹۰", art40, setArt40)}
          {boolRow("واحد تولیدی/آسیب‌دیده", isProd, setIsProd)}
          {boolRow("شرط افزایش ویژه", specialOk, setSpecialOk)}
        </div>
      </section>

      <section className="space-y-2 rounded-2xl border border-slate-700 bg-[var(--card)] p-5">
        <h2 className="font-semibold">جرائم (ریال)</h2>
        {penalties.map((p, i) => (
          <div key={i} className="grid grid-cols-12 gap-2 text-sm">
            <span className="col-span-5 truncate text-slate-300">{p.type}</span>
            <input
              type="number"
              className="col-span-4 rounded border border-slate-600 bg-slate-900 px-2 py-1"
              value={p.amount || ""}
              onChange={(e) => {
                const next = [...penalties];
                next[i] = { ...p, amount: Number(e.target.value) || 0 };
                setPenalties(next);
              }}
            />
            <select
              className="col-span-3 rounded border border-slate-600 bg-slate-900 px-1 py-1"
              value={p.waivable ? "بله" : "خیر"}
              onChange={(e) => {
                const next = [...penalties];
                next[i] = { ...p, waivable: e.target.value === "بله" };
                setPenalties(next);
              }}
            >
              <option value="بله">قابل بخشش</option>
              <option value="خیر">غیرقابل</option>
            </select>
          </div>
        ))}
      </section>

      <button
        type="button"
        onClick={onCalc}
        disabled={loading}
        className="rounded-xl bg-blue-600 px-6 py-3 font-medium hover:bg-blue-500 disabled:opacity-50"
      >
        {loading ? "در حال محاسبه…" : "محاسبه بخشودگی"}
      </button>

      {error && (
        <p className="text-sm text-red-400">
          خطا: {error} — آیا API روی {API} در حال اجرا است؟
        </p>
      )}

      {result && (
        <section className="space-y-2 rounded-2xl border border-green-800 bg-green-950/30 p-5 text-sm">
          <p>
            درصد پایه پس از کسور: {pct(result.base_after_deductions)}
          </p>
          <p>معافیت ماده ۱۹۰: {pct(result.art190_rate)}</p>
          <p>افزایش ویژه: {pct(result.special_add)}</p>
          <p className="text-lg font-bold">درصد نهایی: {pct(result.final_pct)}</p>
          <p>قابل بخشش: {num(result.waivable_sum)} ریال</p>
          <p className="text-red-300">غیرقابل بخشش: {num(result.non_waivable_sum)} ریال</p>
          <p className="text-lg font-bold text-green-300">
            مبلغ بخشودگی پیشنهادی: {num(result.waived_amount)} ریال
          </p>
          <p className="text-xs text-slate-400">
            {String(result.circular_id)} · {String(result.rule_version)}
          </p>
          <p className="text-xs text-amber-200">{String(result.disclaimer)}</p>
        </section>
      )}

      <p className="text-xs text-slate-500">
        مشاور رسمی: ضیاءالدین موسوی جراحی —{" "}
        <a className="text-blue-400" href="tel:+989153068322">
          ۰۹۱۵۳۰۶۸۳۲۲
        </a>
      </p>
    </main>
  );
}
