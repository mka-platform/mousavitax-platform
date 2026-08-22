"use client";

import { useState } from "react";
import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

type Citation = {
  source_id: string;
  title: string;
  score: number;
  snippet?: string;
};

type Msg = { role: "user" | "assistant"; text: string; citations?: Citation[] };

export default function ChatPage() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [messages, setMessages] = useState<Msg[]>([
    {
      role: "assistant",
      text:
        "سلام. پرسش مالیاتی خود را بنویسید. پاسخ بر اساس دانش ایندکس‌شده و با ذکر منبع است. تصمیم نهایی با مشاور رسمی است.",
    },
  ]);

  const send = async () => {
    const q = input.trim();
    if (!q || loading) return;
    setInput("");
    setError("");
    setMessages((m) => [...m, { role: "user", text: q }]);
    setLoading(true);
    try {
      const res = await fetch(`${API}/v1/rag/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q, top_k: 5 }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          text: data.answer || "پاسخی دریافت نشد.",
          citations: data.citations || [],
        },
      ]);
    } catch (e) {
      setError(String(e));
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          text:
            "خطا در ارتباط با سرویس دانش. مطمئن شوید API روی پورت ۸۰۰۰ روشن است و seed_knowledge اجرا شده.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto flex min-h-[70vh] max-w-3xl flex-col gap-4 px-4 py-10" dir="rtl">
      <div>
        <p className="text-xs text-blue-400">RAG · Citation · Human-in-the-loop</p>
        <h1 className="text-2xl font-extrabold md:text-3xl">مشاور هوشمند AI</h1>
        <p className="mt-1 text-sm text-slate-400">
          API: {API} — در صورت خالی بودن دانش، seed را اجرا کنید.
        </p>
      </div>

      <div className="card flex flex-1 flex-col gap-3 overflow-y-auto p-4" style={{ minHeight: 320 }}>
        {messages.map((m, i) => (
          <div
            key={i}
            className={
              m.role === "user"
                ? "mr-8 rounded-2xl bg-blue-600/20 px-4 py-3 text-sm leading-7"
                : "ml-4 rounded-2xl border border-slate-700 bg-slate-900/50 px-4 py-3 text-sm leading-7"
            }
          >
            <div className="whitespace-pre-wrap">{m.text}</div>
            {m.citations && m.citations.length > 0 && (
              <ul className="mt-3 space-y-1 border-t border-slate-700 pt-2 text-xs text-slate-400">
                {m.citations.map((c, j) => (
                  <li key={j}>
                    <span className="text-blue-300">{c.title}</span>
                    {c.score ? ` · score ${c.score.toFixed?.(3) ?? c.score}` : ""}
                    {c.snippet ? ` — ${c.snippet.slice(0, 120)}…` : ""}
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
        {loading && (
          <div className="text-sm text-slate-500">در حال بازیابی دانش…</div>
        )}
      </div>

      {error && <p className="text-xs text-red-400">{error}</p>}

      <div className="flex gap-2">
        <input
          className="flex-1 rounded-xl border border-slate-600 bg-slate-900 px-4 py-3 text-sm outline-none focus:border-blue-500"
          placeholder="مثلاً: شرایط بخشودگی جرائم ماده ۱۹۰ چیست؟"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          disabled={loading}
        />
        <button type="button" className="btn-primary" onClick={send} disabled={loading}>
          ارسال
        </button>
      </div>

      <p className="text-xs text-slate-500">
        HUMAN_REVIEW_REQUIRED · مشاور رسمی:{" "}
        <a className="text-blue-400" href="tel:+989153068322">
          ۰۹۱۵۳۰۶۸۳۲۲
        </a>
        {" · "}
        <Link href="/" className="text-blue-400">
          خانه
        </Link>
      </p>
    </main>
  );
}
