// pages/_app.tsx

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Navbar from "@/components/Navbar/index";
import Footer from "@/components/Footer/Footer";
import "../styles/globals.css";
import { AppProps } from "next/dist/shared/lib/router/router";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Lycée Moderne Antsirabe",
  description: "Etablissement affilié à e-saina",
};

export default function App({ Component, pageProps }: AppProps) {
    return (
        <>
        <Navbar />
            <Component {...pageProps} />
        <Footer />
        </>
    );
}