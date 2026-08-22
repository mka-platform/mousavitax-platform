import Link from "next/link";

const services = [
  {
    title: "محاسبه‌گر بخشودگی جرائم",
    desc: "پیشنهاد سیستمی بر اساس دستورالعمل ۲۰۰/۱۴۰۴/۵۰۴ با تأیید انسان",
    href: "/waiver",
    tag: "ابزار عملیاتی",
    icon: "٪",
  },
  {
    title: "مشاور هوشمند AI",
    desc: "پرسش مالیاتی با RAG و Citation از منابع رسمی",
    href: "/chat",
    tag: "دانش‌محور",
    icon: "AI",
  },
  {
    title: "خدمات تخصصی",
    desc: "اظهارنامه، لایحه دفاعی، سامانه مودیان، ارزش افزوده",
    href: "/services",
    tag: "خدمات",
    icon: "§",
  },
  {
    title: "بازار مشاوران",
    desc: "اتصال به مشاور انسانی تأییدشده برای پرونده‌های حساس",
    href: "/advisors",
    tag: "انسان در حلقه",
    icon: "◎",
  },
];

const trust = [
  { t: "استناد اجباری", d: "هر پاسخ با منبع قابل پیگیری" },
  { t: "قوانین رسمی", d: "اولویت منابع سازمان امور مالیاتی" },
  { t: "نظارت انسان", d: "تصمیم نهایی با مشاور مجاز" },
  { t: "حریم خصوصی", d: "جداسازی داده عمومی و پرونده" },
];

export default function HomePage() {
  return (
    <main>
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="mx-auto grid max-w-6xl gap-10 px-4 py-14 md:grid-cols-2 md:items-center md:py-20">
          <div className="space-y-6">
            <span className="badge">پلتفرم مالیات هوشمند ایران · MKA</span>
            <h1 className="text-3xl font-extrabold leading-[1.6] md:text-5xl">
              مشاوره مالیاتی
              <span className="block bg-gradient-to-l from-blue-400 to-sky-300 bg-clip-text text-transparent">
                دقیق، مستند، قابل دفاع
              </span>
            </h1>
            <p className="max-w-xl text-base leading-8 text-slate-300 md:text-lg">
              ترکیب دانش رسمی، موتور بخشودگی جرائم، و مشاور انسانی — برای مودی،
              حسابدار و تیم حقوقی که به استناد و نتیجه عملی نیاز دارند.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link href="/waiver" className="btn-primary">
                شروع محاسبه بخشودگی
              </Link>
              <Link href="/chat" className="btn-ghost">
                پرسش از مشاور AI
              </Link>
              <a href="tel:+989153068322" className="btn-ghost">
                تماس با مشاور رسمی
              </a>
            </div>
            <p className="text-xs text-slate-500">
              خروجی سیستمی پیشنهاد است و جایگزین رأی سازمان یا مشاور رسمی نیست.
            </p>
          </div>

          <div className="card relative p-6 md:p-8">
            <div className="mb-4 text-xs font-medium text-blue-300">چرا MousaviTax؟</div>
            <ul className="space-y-4">
              {trust.map((x) => (
                <li key={x.t} className="flex gap-3">
                  <span className="mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-blue-600/20 text-xs text-blue-300">
                    ✓
                  </span>
                  <div>
                    <div className="font-semibold text-slate-100">{x.t}</div>
                    <div className="text-sm text-slate-400">{x.d}</div>
                  </div>
                </li>
              ))}
            </ul>
            <div className="mt-6 rounded-xl border border-amber-500/30 bg-amber-500/10 p-4 text-sm leading-7 text-amber-100">
              <strong>ضیاءالدین موسوی جراحی</strong> — مشاور رسمی مالیاتی
              <br />
              لایحه دفاعی و مشاوره آنلاین:{" "}
              <a className="underline" href="tel:+989153068322">
                ۰۹۱۵۳۰۶۸۳۲۲
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Services grid */}
      <section className="mx-auto max-w-6xl px-4 pb-8">
        <div className="mb-6 flex items-end justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold md:text-2xl">خدمات و ابزارها</h2>
            <p className="mt-1 text-sm text-slate-400">طراحی‌شده برای تصمیم‌گیری سریع و مستند</p>
          </div>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {services.map((s) => (
            <Link key={s.href} href={s.href} className="card group flex flex-col p-5 transition">
              <div className="mb-3 flex items-center justify-between">
                <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600/15 text-sm font-bold text-blue-300">
                  {s.icon}
                </span>
                <span className="text-[10px] text-slate-500">{s.tag}</span>
              </div>
              <h3 className="mb-2 font-semibold group-hover:text-blue-300">{s.title}</h3>
              <p className="flex-1 text-sm leading-6 text-slate-400">{s.desc}</p>
              <span className="mt-4 text-xs text-blue-400">ورود ←</span>
            </Link>
          ))}
        </div>
      </section>

      {/* CTA band */}
      <section className="mx-auto max-w-6xl px-4 py-10">
        <div className="card flex flex-col items-start justify-between gap-6 bg-gradient-to-l from-blue-950/50 to-slate-900/40 p-8 md:flex-row md:items-center">
          <div>
            <h2 className="text-xl font-bold">آماده بررسی پرونده یا جرائم خود هستید؟</h2>
            <p className="mt-2 max-w-xl text-sm leading-7 text-slate-300">
              از محاسبه‌گر بخشودگی شروع کنید یا مستقیم با مشاور رسمی هماهنگ شوید.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <Link href="/waiver" className="btn-primary">
              محاسبه بخشودگی
            </Link>
            <a href="tel:+989153068322" className="btn-ghost">
              ۰۹۱۵۳۰۶۸۳۲۲
            </a>
          </div>
        </div>
      </section>
    </main>
  );
}
