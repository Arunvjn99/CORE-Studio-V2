import type { Metadata } from "next";
import { Toaster } from "sonner";
import { Providers } from "./providers";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "CORE Studio — AI Design Office",
  description: "AI-powered digital product office. Design with intelligence.",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body>
        <Providers>
          {children}
          <Toaster
            position="bottom-right"
            toastOptions={{
              style: {
                fontFamily: "Inter, sans-serif",
                fontSize: "13px",
              },
            }}
          />
        </Providers>
      </body>
    </html>
  );
}
