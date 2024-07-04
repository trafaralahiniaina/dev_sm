// src/pages/contact.tsx

import React from 'react';
import MainLayout from '../../components/layouts/Mainlayout';

const Activites: React.FC = () => {
  return (
    <MainLayout>
      <div className='flex min-h-screen flex-col items-center justify-between p-10 mt-20 md:mt-28'>
        <h1 className='text-6xl font-bold'>Activités</h1>
        <p className='text-2xl mt-4'>Nous sommes disponibles pour répondre à vos questions.</p>
      </div>
    </MainLayout>
  );
};

export default Activites;