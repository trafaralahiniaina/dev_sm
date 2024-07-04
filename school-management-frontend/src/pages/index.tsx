// src\pages\acceuil.tsx

import React, { useEffect } from 'react';
import { useSchools } from '../hooks/useSchool';
import SchoolList from '../components/schools/SchoolList';
import MainLayout from '../components/layouts/Mainlayout';

const Index: React.FC = () => {
  const { schools, fetchSchools } = useSchools();

  useEffect(() => {
    fetchSchools();
  }, [fetchSchools]);

  return (
    <>
      <MainLayout title="Accueil | e-anatra">
        <div className="flex min-h-screen flex-col items-center justify-between p-10 mt-20 md:mt-28">
          <h1 className="text-6xl font-bold">Bienvenue sur notre site !</h1>
          <p className="text-2xl">Nous sommes ravis de vous accueillir.</p>
          <SchoolList schools={schools} />
        </div>
      </MainLayout>
    </> 
  );
};

export default Index;