import React from 'react';
import Head from 'next/head';
import Header from './Header';
import Footer from './Footer';
import { School } from '@/types/school';

interface LayoutProps {
  school: School;
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ school, children }) => {
  return (
    <>
      <Head>
        <title>{school.name}</title>
        <link rel="icon" href="/favicon.ico" />
        <link rel="stylesheet" href={`/styles/${school.website.split('.')[0]}/styles.css`} />
      </Head>
      <Header school={school} />
      <main>{children}</main>
      <Footer school={school} />
    </>
  );
};

export default Layout;