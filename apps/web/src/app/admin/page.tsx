"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

type Tab = "advisors" | "careers" | "waivers";

export default function AdminPage() {
  const [tab, setTab] = useState<Tab>("advisors");
  const [items, setItems] = useState<Record<string, unknown>[]>([]);
  const [count, setCount] = useState(0);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const path =
        tab === "advisors"
          ? "/v1/advisors/requests"
          : tab === "careers"
            ? "/v1/careers/applications"
            : "/v1/tax/waiver/logs";
      const res = await fetch(`${API}${path}`);
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setItems(data.items || []);
      setCount(data.count || 0);
    } catch (e) {
      setError(String(e));
      setItems([]);
      setCount(0);
    } finally {
      setLoading(false);
    }
  }, [tab]);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <main className="mx-auto max-w-4xl space-y-6 px-4 py-10" dir="rtl">
      <div>
        <p className="text-xs text-amber-400">MVP · بدون لاگین — فقط شبکه محلی / مدیر</p>
        <h1 className="text-2xl font-extrabold">پنل بررسی درخواست‌ها</h1>
        <p className="mt-1 text-sm text-slate-400">
          مشاورین، استخدام، لاگ بخشودگی — برای بررسی انسانی
        </p>
      </div>

      <div className="flex flex-wrap gap-2">
        {(
          [
            ["advisors", "مشاورین / اعتبارسنجی"],
            ["careers", "استخدام"],
            ["waivers", "لاگ بخشودگی"],
          ] as const
        ).map(([k, label]) => (
          <button
            key={k}
            type="button"
            className={`rounded-xl px-4 py-2 text-sm ${tab === k ? "bg-blue-600 text-white" : "border border-slate-600 text-slate-300"}`}
            onClick={() => setTab(k)}
          >
            {label}
          </button>
        ))}
        <button type="button" className="btn-ghost text-sm" onClick={load} disabled={loading}>
          {loading ? "…" : "بروزرسانی"}
        </button>
      </div>

      {error && <p className="text-sm text-red-400">{error}</p>}
      <p className="text-xs text-slate-500">تعداد: {count}</p>

      <div className="space-y-3">
        {items.length === 0 && !loading && (
          <div className="card p-6 text-sm text-slate-400">موردی ثبت نشده است.</div>
        )}
        {items.map((it, i) => (
          <div key={String(it.id || i)} className="card space-y-1 p-4 text-sm">
            <div className="flex flex-wrap justify-between gap-2">
              <span className="font-semibold text-blue-300">{String(it.id || "—")}</span>
              <span className="text-xs text-slate-500">{String(it.created_at || "")}</span>
            </div>
            <pre className="overflow-x-auto whitespace-pre-wrap text-xs leading-6 text-slate-300">
              {JSON.stringify(it, null, 2)}
            </pre>
          </div>
        ))}
      </div>

      <Link href="/" className="text-sm text-blue-400">
        خانه
      </Link>
    </main>
  );
}
