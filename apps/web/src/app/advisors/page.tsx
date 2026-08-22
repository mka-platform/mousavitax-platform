"use client";

import { useState } from "react";
import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function AdvisorsPage() {
  const [fullName, setFullName] = useState("");
  const [mobile, setMobile] = useState("");
  const [city, setCity] = useState("");
  const [topic, setTopic] = useState("مشاوره عمومی");
  const [details, setDetails] = useState("");
  const [preferredTime, setPreferredTime] = useState("");
  const [role, setRole] = useState("مودی");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ ok?: boolean; id?: string; message?: string } | null>(null);
  const [error, setError] = useState("");

  const submit = async () => {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await fetch(`${API}/v1/advisors/request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          full_name: fullName,
          mobile,
          city,
          topic,
          details,
          preferred_time: preferredTime,
          role,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      setResult(await res.json());
      setDetails("");
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto max-w-2xl space-y-6 px-4 py-10" dir="rtl">
      <div>
        <p className="text-xs text-blue-400">بازار مشاوران · Human-in-the-loop</p>
        <h1 className="text-2xl font-extrabold md:text-3xl">درخواست مشاوره انسانی</h1>
        <p className="mt-2 text-sm leading-7 text-slate-400">
          برای پرونده‌های حساس، لایحه دفاعی یا بررسی خروجی AI، درخواست خود را ثبت کنید.
          پیگیری توسط تیم مشاور (ضیاءالدین موسوی جراحی).
        </p>
      </div>

      <div className="card space-y-4 p-6">
        <label className="block text-sm">
          نقش
          <select
            className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <option>مودی</option>
            <option>حسابدار</option>
            <option>مشاور (ثبت‌نام همکاری)</option>
          </select>
        </label>
        <label className="block text-sm">
          نام و نام خانوادگی *
          <input
            className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />
        </label>
        <label className="block text-sm">
          موبایل *
          <input
            className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2"
            placeholder="09xxxxxxxxx"
            value={mobile}
            onChange={(e) => setMobile(e.target.value)}
          />
        </label>
        <label className="block text-sm">
          شهر
          <input
            className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />
        </label>
        <label className="block text-sm">
          موضوع
          <select
            className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          >
            <option>مشاوره عمومی</option>
            <option>بخشودگی جرائم</option>
            <option>لایحه دفاعی</option>
            <option>ارزش افزوده</option>
            <option>سامانه مودیان</option>
            <option>عملکرد / تشخیص</option>
            <option>سایر</option>
          </select>
        </label>
        <label className="block text-sm">
          زمان ترجیحی تماس
          <input
            className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2"
            placeholder="مثلاً فردا عصر"
            value={preferredTime}
            onChange={(e) => setPreferredTime(e.target.value)}
          />
        </label>
        <label className="block text-sm">
          شرح مختصر
          <textarea
            className="mt-1 min-h-[100px] w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2"
            value={details}
            onChange={(e) => setDetails(e.target.value)}
          />
        </label>
        <button
          type="button"
          className="btn-primary w-full"
          disabled={loading || !fullName.trim() || !mobile.trim()}
          onClick={submit}
        >
          {loading ? "در حال ثبت…" : "ثبت درخواست"}
        </button>
        {error && <p className="text-sm text-red-400">{error}</p>}
        {result?.ok && (
          <div className="rounded-xl border border-green-700/50 bg-green-950/40 p-4 text-sm text-green-100">
            {result.message}
            <div className="mt-1 text-xs text-slate-400">کد پیگیری: {result.id}</div>
          </div>
        )}
      </div>

      <div className="card p-5 text-sm leading-7 text-slate-300">
        تماس مستقیم با مشاور رسمی:{" "}
        <a className="text-blue-400" href="tel:+989153068322">
          ۰۹۱۵۳۰۶۸۳۲۲
        </a>
      </div>
      <Link href="/" className="text-sm text-blue-400">
        بازگشت به خانه
      </Link>
    </main>
  );
}
