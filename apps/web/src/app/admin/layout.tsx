import Link from "next/link";
import type { ReactNode } from "react";

const nav = [
  { href: "/admin", label: "داشبورد" },
  { href: "/admin/cases", label: "پرونده‌ها (Cases)" },
  { href: "/admin/advisors", label: "مشاورین" },
  { href: "/admin/careers", label: "استخدام" },
  { href: "/admin/waiver", label: "لاگ بخشودگی" },
  { href: "/admin/ledger", label: "دفترکل (Ledger)" },
  { href: "/admin/audit", label: "ممیزی (Audit)" },
];

export default function AdminLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100" dir="rtl">
      <div className="border-b border-slate-800 bg-[#0a101c]/95">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-4 py-3">
          <div>
            <div className="text-sm font-bold">MousaviTax · Central Admin</div>
            <div className="text-[10px] text-amber-400/90">
              عملیات از API Gateway · امنیت فقط در Backend
            </div>
          </div>
          <Link href="/" className="text-xs text-blue-400 hover:underline">
            بازگشت به سایت
          </Link>
        </div>
      </div>
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-4 py-6 md:flex-row">
        <aside className="w-full shrink-0 md:w-52">
          <nav className="flex flex-row flex-wrap gap-1 md:flex-col">
            {nav.map((n) => (
              <Link
                key={n.href}
                href={n.href}
                className="rounded-lg px-3 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white"
              >
                {n.label}
              </Link>
            ))}
          </nav>
        </aside>
        <main className="min-w-0 flex-1">{children}</main>
      </div>
    </div>
  );
}
