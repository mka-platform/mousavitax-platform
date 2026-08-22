import Link from "next/link";

export default function Page() {
  return (
    <main className="mx-auto max-w-3xl space-y-6 px-4 py-12" dir="rtl">
      <p className="text-xs text-blue-400">MousaviTax · MKA</p>
      <h1 className="text-2xl font-extrabold md:text-3xl">مشاور هوشمند AI</h1>
      <p className="leading-8 text-slate-300">پرسش مالیاتی با استناد (RAG). در حال اتصال به دانش رسمی Drive.</p>
      <div className="card space-y-3 p-6 text-sm text-slate-300">
        <p>برای اقدام فوری با مشاور رسمی تماس بگیرید:</p>
        <a className="btn-primary inline-flex" href="tel:+989153068322">۰۹۱۵۳۰۶۸۳۲۲</a>
        <p className="text-xs text-slate-500">ضیاءالدین موسوی جراحی — مشاور رسمی مالیاتی</p>
      </div>
      <Link href="/" className="text-sm text-blue-400">بازگشت به خانه</Link>
    </main>
  );
}
