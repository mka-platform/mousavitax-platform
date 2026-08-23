import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "MousaviTax | مشاوره مالیاتی هوشمند",
  description:
    "پلتفرم مشاوره و خدمات مالیاتی هوشمند ایران — دانش رسمی، استناد، مشاور انسانی. ضیاءالدین موسوی جراحی",
};

const nav = [
  { href: "/", label: "خانه" },
  { href: "/waiver", label: "بخشودگی جرائم" },
  { href: "/chat", label: "مشاور AI" },
  { href: "/services", label: "خدمات" },
  { href: "/advisors", label: "ارتباط با مشاورین" },
  { href: "/careers", label: "استخدام" },
  { href: "/admin", label: "پنل مدیر" },
];

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="fa" dir="rtl">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen antialiased">
        <header className="sticky top-0 z-40 border-b border-slate-800/80 bg-[#070b14]/85 backdrop-blur-md">
          <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
            <Link href="/" className="flex items-center gap-2">
              <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 text-sm font-bold">
                MT
              </span>
              <div className="leading-tight">
                <div className="text-sm font-bold tracking-tight">MousaviTax</div>
                <div className="text-[10px] text-slate-400">MKA · ARYA Holding</div>
              </div>
            </Link>
            <nav className="hidden items-center gap-1 md:flex">
              {nav.map((n) => (
                <Link
                  key={n.href}
                  href={n.href}
                  className="rounded-lg px-3 py-2 text-sm text-slate-300 transition hover:bg-slate-800 hover:text-white"
                >
                  {n.label}
                </Link>
              ))}
            </nav>
            <a href="tel:+989153068322" className="btn-primary text-xs md:text-sm">
              مشاوره: ۰۹۱۵۳۰۶۸۳۲۲
            </a>
          </div>
        </header>

        {children}

        <footer className="mt-16 border-t border-slate-800 bg-[#0a101c]">
          <div className="mx-auto grid max-w-6xl gap-8 px-4 py-10 md:grid-cols-3">
            <div>
              <div className="mb-2 font-bold">MousaviTax</div>
              <p className="text-sm leading-7 text-slate-400">
                هسته هوشمند دانش مالیاتی با استناد اجباری و نظارت انسان.
                جایگزین مشاور رسمی یا وکیل نیست.
              </p>
            </div>
            <div>
              <div className="mb-2 text-sm font-semibold text-slate-200">دسترسی سریع</div>
              <ul className="space-y-2 text-sm text-slate-400">
                {nav.map((n) => (
                  <li key={n.href}>
                    <Link href={n.href} className="hover:text-blue-400">
                      {n.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <div className="mb-2 text-sm font-semibold text-slate-200">مشاور رسمی</div>
              <p className="text-sm leading-7 text-slate-400">
                ضیاءالدین موسوی جراحی
                <br />
                <a className="text-blue-400" href="tel:+989153068322">
                  ۰۹۱۵۳۰۶۸۳۲۲
                </a>
                <br />
                ziya.mka2026@gmail.com
              </p>
            </div>
          </div>
          <div className="border-t border-slate-800 py-4 text-center text-xs text-slate-500">
            © {new Date().getFullYear()} MKA / ARYA Holding — کلیه حقوق متعلق به مالک پروژه است.
          </div>
        </footer>
      </body>
    </html>
  );
}
