// pages/_app.tsx

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Navbar from "@/components/mainNavbar/index";
import Footer from "@/components/mainFooter/Footer";
import "../styles/globals.css";
import { AppProps } from "next/dist/shared/lib/router/router";
import MainLayout from "@/components/layouts/Mainlayout";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "e-anatra",
  description: "L'éducation 2.0",
};

export default function App({ Component, pageProps }: AppProps) {
    return (
        <Component {...pageProps} />

    );
}