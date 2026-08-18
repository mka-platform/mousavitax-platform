import Link from "next/link";

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-5xl flex-col gap-10 px-4 py-12">
      <header className="space-y-3">
        <p className="text-sm text-blue-400">MKA / ARYA Holding · APCS v1.0</p>
        <h1 className="text-3xl font-bold leading-relaxed md:text-4xl">
          MousaviTax Platform
        </h1>
        <p className="max-w-2xl text-slate-300 leading-8">
          پلتفرم مشاوره و خدمات مالیاتی هوشمند ایران — ترکیب دانش رسمی، Citation
          اجباری، و مشاور انسانی.
        </p>
      </header>

      <section className="grid gap-4 md:grid-cols-3">
        {[
          {
            title: "چت مشاور AI",
            desc: "پرسش مالیاتی با استناد به منابع (RAG + APCS)",
            href: "/chat",
          },
          {
            title: "بازار مشاوران",
            desc: "درخواست مشاوره تلفنی و تخصصی از مشاوران انسانی",
            href: "/advisors",
          },
          {
            title: "خدمات عملیاتی",
            desc: "اظهارنامه، لایحه دفاعیه، سامانه مودیان",
            href: "/services",
          },
        ].map((c) => (
          <Link
            key={c.href}
            href={c.href}
            className="rounded-2xl border border-slate-700 bg-[var(--card)] p-5 transition hover:border-blue-500"
          >
            <h2 className="mb-2 text-lg font-semibold">{c.title}</h2>
            <p className="text-sm text-slate-400 leading-6">{c.desc}</p>
          </Link>
        ))}
      </section>

      <footer className="text-xs text-slate-500 leading-6">
        این سامانه جایگزین مشاور رسمی مالیاتی یا وکیل نیست. تصمیم نهایی با مودی و
        مشاور مجاز است.
      </footer>
    </main>
  );
}
