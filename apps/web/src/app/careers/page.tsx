"use client";

import { useState } from "react";
import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

const ROLES = [
  "کارشناس مالیاتی",
  "کارشناس لایحه و دفاع",
  "حسابدار",
  "پشتیبان سامانه / داده",
  "توسعه‌دهنده نرم‌افزار",
  "سایر",
];

export default function CareersPage() {
  const [fullName, setFullName] = useState("");
  const [mobile, setMobile] = useState("");
  const [email, setEmail] = useState("");
  const [city, setCity] = useState("");
  const [role, setRole] = useState(ROLES[0]);
  const [experienceYears, setExperienceYears] = useState("0");
  const [education, setEducation] = useState("");
  const [resumeSummary, setResumeSummary] = useState("");
  const [availability, setAvailability] = useState("تمام‌وقت");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ ok?: boolean; id?: string; message?: string } | null>(null);
  const [error, setError] = useState("");

  const submit = async () => {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await fetch(`${API}/v1/careers/apply`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          full_name: fullName,
          mobile,
          email,
          city,
          desired_role: role,
          experience_years: Number(experienceYears) || 0,
          education,
          resume_summary: resumeSummary,
          availability,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      setResult(await res.json());
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto max-w-2xl space-y-6 px-4 py-10" dir="rtl">
      <div>
        <p className="text-xs text-blue-400">منابع انسانی · MousaviTax / MKA</p>
        <h1 className="text-2xl font-extrabold md:text-3xl">درخواست کار و استخدام کارمند</h1>
        <p className="mt-2 text-sm leading-7 text-slate-400">
          رزومه و درخواست همکاری را ثبت کنید. بررسی توسط مدیریت انجام می‌شود و
          نتیجه از طریق تماس اعلام خواهد شد.
        </p>
      </div>

      <div className="card space-y-4 p-6">
        <label className="block text-sm">
          نام و نام خانوادگی *
          <input className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={fullName} onChange={(e) => setFullName(e.target.value)} />
        </label>
        <label className="block text-sm">
          موبایل *
          <input className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={mobile} onChange={(e) => setMobile(e.target.value)} />
        </label>
        <label className="block text-sm">
          ایمیل
          <input className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <label className="block text-sm">
          شهر
          <input className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={city} onChange={(e) => setCity(e.target.value)} />
        </label>
        <label className="block text-sm">
          سمت مورد نظر
          <select className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={role} onChange={(e) => setRole(e.target.value)}>
            {ROLES.map((r) => (
              <option key={r}>{r}</option>
            ))}
          </select>
        </label>
        <label className="block text-sm">
          سابقه کار (سال)
          <input type="number" className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={experienceYears} onChange={(e) => setExperienceYears(e.target.value)} />
        </label>
        <label className="block text-sm">
          آخرین مدرک تحصیلی
          <input className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={education} onChange={(e) => setEducation(e.target.value)} />
        </label>
        <label className="block text-sm">
          نوع همکاری
          <select className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={availability} onChange={(e) => setAvailability(e.target.value)}>
            <option>تمام‌وقت</option>
            <option>پاره‌وقت</option>
            <option>دورکاری</option>
            <option>پروژه‌ای</option>
          </select>
        </label>
        <label className="block text-sm">
          خلاصه رزومه و مهارت‌ها *
          <textarea className="mt-1 min-h-[120px] w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={resumeSummary} onChange={(e) => setResumeSummary(e.target.value)} />
        </label>
        <button
          type="button"
          className="btn-primary w-full"
          disabled={loading || !fullName.trim() || !mobile.trim() || !resumeSummary.trim()}
          onClick={submit}
        >
          {loading ? "در حال ارسال…" : "ارسال درخواست استخدام"}
        </button>
        {error && <p className="text-sm text-red-400">{error}</p>}
        {result?.ok && (
          <div className="rounded-xl border border-green-700/50 bg-green-950/40 p-4 text-sm text-green-100">
            {result.message}
            <div className="mt-1 text-xs text-slate-400">کد پیگیری: {result.id}</div>
          </div>
        )}
      </div>

      <Link href="/" className="text-sm text-blue-400">
        بازگشت به خانه
      </Link>
    </main>
  );
}
