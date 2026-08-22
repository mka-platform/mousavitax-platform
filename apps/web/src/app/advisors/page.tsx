"use client";

import { useState } from "react";
import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

/** فیلدهای اعتبارسنجی مطابق حاکمیت مدارک (عنوان شغلی + شناسه حرفه‌ای) */
const DOC_TYPES = [
  "پروانه مشاور رسمی مالیاتی",
  "پروانه وکالت دادگستری",
  "کارت عضویت جامعه حسابداران رسمی",
  "مدرک تحصیلی مرتبط",
  "سایر مدارک حرفه‌ای",
];

export default function AdvisorsPage() {
  const [mode, setMode] = useState<"client" | "professional">("client");
  const [fullName, setFullName] = useState("");
  const [mobile, setMobile] = useState("");
  const [city, setCity] = useState("");
  const [topic, setTopic] = useState("مشاوره عمومی");
  const [details, setDetails] = useState("");
  const [preferredTime, setPreferredTime] = useState("");
  // professional verification
  const [title, setTitle] = useState("مشاور رسمی مالیاتی");
  const [licenseNo, setLicenseNo] = useState("");
  const [docType, setDocType] = useState(DOC_TYPES[0]);
  const [docRef, setDocRef] = useState("");
  const [orgName, setOrgName] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ ok?: boolean; id?: string; message?: string; verification_status?: string } | null>(null);
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
          role: mode === "client" ? "مودی" : "مشاور (ثبت‌نام همکاری)",
          professional_title: mode === "professional" ? title : "",
          license_number: mode === "professional" ? licenseNo : "",
          document_type: mode === "professional" ? docType : "",
          document_reference: mode === "professional" ? docRef : "",
          organization: mode === "professional" ? orgName : "",
          credentials_submitted: mode === "professional",
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
        <p className="text-xs text-blue-400">اعتبارسنجی مدارک · مشاورین حقیقی و حقوقی</p>
        <h1 className="text-2xl font-extrabold md:text-3xl">ارتباط با مشاورین حقیقی و حقوقی</h1>
        <p className="mt-2 text-sm leading-7 text-slate-400">
          درخواست مشاوره یا ثبت‌نام همکاری. عناوین و مدارک حرفه‌ای پس از بررسی انسانی
          (طبق مستندات حاکمیتی پروژه) تأیید یا رد می‌شوند — وضعیت اولیه همیشه
          «در انتظار اعتبارسنجی» است.
        </p>
      </div>

      <div className="flex gap-2">
        <button
          type="button"
          className={`rounded-xl px-4 py-2 text-sm ${mode === "client" ? "bg-blue-600 text-white" : "border border-slate-600 text-slate-300"}`}
          onClick={() => setMode("client")}
        >
          درخواست مشاوره (مودی)
        </button>
        <button
          type="button"
          className={`rounded-xl px-4 py-2 text-sm ${mode === "professional" ? "bg-blue-600 text-white" : "border border-slate-600 text-slate-300"}`}
          onClick={() => setMode("professional")}
        >
          ثبت‌نام مشاور حقیقی / حقوقی
        </button>
      </div>

      <div className="card space-y-4 p-6">
        <label className="block text-sm">
          نام و نام خانوادگی *
          <input className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={fullName} onChange={(e) => setFullName(e.target.value)} />
        </label>
        <label className="block text-sm">
          موبایل *
          <input className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={mobile} onChange={(e) => setMobile(e.target.value)} placeholder="09xxxxxxxxx" />
        </label>
        <label className="block text-sm">
          شهر
          <input className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={city} onChange={(e) => setCity(e.target.value)} />
        </label>

        {mode === "client" ? (
          <>
            <label className="block text-sm">
              موضوع
              <select className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={topic} onChange={(e) => setTopic(e.target.value)}>
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
              <input className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={preferredTime} onChange={(e) => setPreferredTime(e.target.value)} />
            </label>
          </>
        ) : (
          <>
            <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-xs leading-6 text-amber-100">
              اعتبارسنجی: شماره پروانه/مجوز و نوع مدرک ثبت می‌شود. تأیید نهایی فقط پس از
              بررسی انسان (مدیر/مالک). بارگذاری فایل کامل بعداً به Drive امن متصل می‌شود؛
              فعلاً شناسه و مشخصات مدرک الزامی است.
            </div>
            <label className="block text-sm">
              عنوان حرفه‌ای *
              <select className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={title} onChange={(e) => setTitle(e.target.value)}>
                <option>مشاور رسمی مالیاتی</option>
                <option>وکیل دادگستری</option>
                <option>حسابدار رسمی</option>
                <option>کارشناس رسمی دادگستری</option>
                <option>سایر متخصص حقوقی/مالیاتی</option>
              </select>
            </label>
            <label className="block text-sm">
              شماره پروانه / مجوز *
              <input className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={licenseNo} onChange={(e) => setLicenseNo(e.target.value)} />
            </label>
            <label className="block text-sm">
              نوع مدرک برای اعتبارسنجی *
              <select className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={docType} onChange={(e) => setDocType(e.target.value)}>
                {DOC_TYPES.map((d) => (
                  <option key={d}>{d}</option>
                ))}
              </select>
            </label>
            <label className="block text-sm">
              شناسه / کد رهگیری مدرک
              <input className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={docRef} onChange={(e) => setDocRef(e.target.value)} placeholder="شماره نامه یا کد استعلام" />
            </label>
            <label className="block text-sm">
              مؤسسه / دفتر
              <input className="mt-1 w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={orgName} onChange={(e) => setOrgName(e.target.value)} />
            </label>
          </>
        )}

        <label className="block text-sm">
          شرح
          <textarea className="mt-1 min-h-[90px] w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2" value={details} onChange={(e) => setDetails(e.target.value)} />
        </label>

        <button
          type="button"
          className="btn-primary w-full"
          disabled={
            loading ||
            !fullName.trim() ||
            !mobile.trim() ||
            (mode === "professional" && !licenseNo.trim())
          }
          onClick={submit}
        >
          {loading ? "در حال ثبت…" : mode === "client" ? "ثبت درخواست مشاوره" : "ارسال برای اعتبارسنجی"}
        </button>

        {error && <p className="text-sm text-red-400">{error}</p>}
        {result?.ok && (
          <div className="rounded-xl border border-green-700/50 bg-green-950/40 p-4 text-sm text-green-100">
            {result.message}
            <div className="mt-1 text-xs text-slate-400">کد: {result.id}</div>
            {result.verification_status && (
              <div className="mt-1 text-xs text-amber-200">وضعیت اعتبارسنجی: {result.verification_status}</div>
            )}
          </div>
        )}
      </div>

      <p className="text-xs text-slate-500">
        تماس مستقیم:{" "}
        <a className="text-blue-400" href="tel:+989153068322">
          ۰۹۱۵۳۰۶۸۳۲۲
        </a>{" "}
        ·{" "}
        <Link href="/careers" className="text-blue-400">
          درگاه استخدام
        </Link>{" "}
        ·{" "}
        <Link href="/" className="text-blue-400">
          خانه
        </Link>
      </p>
    </main>
  );
}
