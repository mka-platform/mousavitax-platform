"use client";

import { FormEvent, useState } from "react";

type Citation = {
  title: string;
  score?: number;
  page?: number;
};

type RagResponse = {
  answer: string;
  citations: Citation[];
  model?: string;
  latency_ms?: number;
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ChatPage() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RagResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/v1/rag/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, top_k: 5 }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = (await res.json()) as RagResponse;
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "خطا در ارتباط با API");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-3xl px-4 py-10">
      <h1 className="mb-6 text-2xl font-bold">چت مشاور مالیاتی</h1>
      <form onSubmit={onSubmit} className="space-y-4">
        <textarea
          className="w-full rounded-xl border border-slate-700 bg-[var(--card)] p-4 text-sm leading-7 outline-none focus:border-blue-500"
          rows={4}
          placeholder="سوال مالیاتی خود را بنویسید..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-medium disabled:opacity-50"
        >
          {loading ? "در حال پاسخ..." : "ارسال"}
        </button>
      </form>

      {error && <p className="mt-4 text-sm text-red-400">{error}</p>}

      {result && (
        <section className="mt-8 space-y-4 rounded-2xl border border-slate-700 bg-[var(--card)] p-5">
          <div className="whitespace-pre-wrap text-sm leading-8">{result.answer}</div>
          {result.citations?.length > 0 && (
            <div className="border-t border-slate-700 pt-4">
              <h2 className="mb-2 text-sm font-semibold text-slate-300">منابع</h2>
              <ul className="space-y-1 text-xs text-slate-400">
                {result.citations.map((c, i) => (
                  <li key={i}>
                    {i + 1}. {c.title}
                    {c.page != null ? ` — صفحه ${c.page}` : ""}
                  </li>
                ))}
              </ul>
            </div>
          )}
          {(result.model || result.latency_ms) && (
            <p className="text-xs text-slate-500">
              {result.model} {result.latency_ms != null ? `· ${result.latency_ms}ms` : ""}
            </p>
          )}
        </section>
      )}
    </main>
  );
}
