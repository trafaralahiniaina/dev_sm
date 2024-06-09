//src/app/layout.tsx

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Navbar from "@/components/Navbar/index";
import Footer from "@/components/Footer/Footer";
import "../styles/globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Lycée Moderne Antsirabe",
  description: "Etablissement affilié à e-saina",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        {children}
        <Footer />
      </body>
    </html>
  );
}
