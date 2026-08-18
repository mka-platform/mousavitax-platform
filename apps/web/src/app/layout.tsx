import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MousaviTax | مشاوره مالیاتی هوشمند",
  description: "پلتفرم مشاوره و خدمات مالیاتی هوشمند ایران — MKA / ARYA Holding",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="fa" dir="rtl">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
