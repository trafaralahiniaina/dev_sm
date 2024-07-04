import React from 'react';
import Head from 'next/head';
import Navbar from '../mainNavbar';
import Footer from '../mainFooter/Footer';

interface MainLayoutProps {
  children: React.ReactNode;
  title?: string;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children, title = 'e-anatra' }) => {
  return (
    <div className="flex flex-col min-h-screen">
      <Head>
        <title>{title}</title>
        <meta name="description" content="Plateforme de gestion scolaire e-anatra" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="flex-grow container mx-auto px-4 py-8">
        <Navbar/>
          {children}
        <Footer/>
      </main>
    </div>
  );
};

export default MainLayout;