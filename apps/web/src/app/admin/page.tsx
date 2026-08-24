"use client";

import { useEffect, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

type Summary = Record<string, number | string | null> | null;

const CARDS = [
  { key: "customers", label: "Customers" },
  { key: "cases", label: "Cases" },
  { key: "human_reviews", label: "Human Reviews" },
  { key: "machine_orders", label: "Machine Orders" },
  { key: "human_services", label: "Human Services" },
  { key: "revenue", label: "Revenue" },
  { key: "ai_services", label: "AI Services" },
  { key: "advisors", label: "Advisors" },
  { key: "pending", label: "Pending" },
] as const;

export default function AdminDashboardPage() {
  const [data, setData] = useState<Summary>(null);
  const [state, setState] = useState<"loading" | "ok" | "empty" | "error" | "unauthorized">(
    "loading"
  );
  const [error, setError] = useState("");

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("mka_token") : null;
    fetch(`${API}/v1/admin/dashboard/summary`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    })
      .then(async (r) => {
        if (r.status === 401 || r.status === 403) {
          setState("unauthorized");
          return;
        }
        if (!r.ok) throw new Error(await r.text());
        const j = await r.json();
        setData(j);
        setState("ok");
      })
      .catch((e) => {
        setError(String(e));
        setState("error");
      });
  }, []);

  return (
    <div className="space-y-6" dir="rtl">
      <div>
        <h1 className="text-2xl font-extrabold">Admin Dashboard</h1>
        <p className="text-sm text-slate-400">
          داده فقط از API · بدون عدد جعلی · Ledger منبع مالی رسمی
        </p>
      </div>

      {state === "loading" && <p className="text-sm text-slate-500">در حال بارگذاری…</p>}
      {state === "unauthorized" && (
        <p className="rounded-xl border border-amber-600/40 bg-amber-950/30 p-4 text-sm text-amber-100">
          نیاز به ورود (Bearer token). امنیت در Backend است، نه فقط UI.
        </p>
      )}
      {state === "error" && <p className="text-sm text-red-400">{error}</p>}

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {CARDS.map((c) => {
          const v = data?.[c.key];
          const display =
            state !== "ok" || v === undefined || v === null || v === "" ? "—" : String(v);
          return (
            <div key={c.key} className="rounded-2xl border border-slate-700 bg-[#121a2c] p-4">
              <div className="text-xs text-slate-500">{c.label}</div>
              <div className="mt-2 text-2xl font-bold tabular-nums">{display}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
