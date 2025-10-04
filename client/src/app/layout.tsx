import type { Metadata } from "next";
import "./globals.css";
import LayoutClient from "@/components/LayoutClient";
import { ThemeScript } from "@/components/ThemeScript";

export const metadata: Metadata = {
  title: {
    absolute: "FINAM_HACKATHON",
    template: "%s | NullPointerException",
  },
  description: "FINAM_HACKATHON",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru" suppressHydrationWarning>
      <head>
        <ThemeScript />
      </head>
      <body className={`antialiased`}>
        <LayoutClient>{children}</LayoutClient>
      </body>
    </html>
  );
}
