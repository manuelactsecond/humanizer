import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Humanizer - AI Text Detection & Humanization",
  description:
    "Detect AI-generated text and transform it to sound naturally human-written. Supports Spanish (Spain) and English (US/UK).",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-foreground min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}
