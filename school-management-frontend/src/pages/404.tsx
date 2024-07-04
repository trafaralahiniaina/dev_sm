// src/pages/404.tsx

import React from 'react';
import MainLayout from '../components/layouts/Mainlayout';
import Link from 'next/link';

const NotFoundPage = () => {
  return (
    <MainLayout title="Page non trouvée | e-anatra">
      <div className="container mx-auto p-10 mt-20 md:mt-28 text-center">
        <h1 className="text-6xl font-bold mb-8">404</h1>
        <p className="text-2xl mb-4">Page non trouvée</p>
        <Link href="/" className="text-blue-500 underline">
          Retour à la page d&apos;accueil
        </Link>
      </div>
    </MainLayout>
  );
};

export default NotFoundPage;