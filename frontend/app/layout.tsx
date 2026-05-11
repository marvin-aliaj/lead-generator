import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "WiFi Portal",
  description: "Restaurant WiFi Portal & Feedback System",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
