import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Sidebar from "./components/sidebar/Sidebar";
import Header from "./components/header/Header";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "DSEnv",
  description: "Digital Sovereignty Evaluation Tool",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="de">
      <body className={inter.className}>
        <div className="flex flex-row bg-gray-900 h-dvh">
          <Sidebar />
          <div className="flex-col grow">
            <Header />
            <main className="bg-red-400 rounded-tl-lg pt-3 pl-3 h-dvh">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
