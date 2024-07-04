// src\pages\[schoolDomain]\index.tsx

import { GetServerSideProps } from 'next';
import React, { useEffect } from 'react';
import { useSchool } from '../../hooks/useSchool';
import MainLayout from '../../components/layouts/Mainlayout';
import { School } from '../../types';
import Image from 'next/image';

interface SchoolPageProps {
  school: School | null;
  schoolDomain: string;
}

 const SchoolPage: React.FC<SchoolPageProps> = ({ school, schoolDomain }) => {
  const { school: fetchedSchool, error, loading, fetchSchool } = useSchool(schoolDomain);

  useEffect(() => {
    if (!school) {
      fetchSchool();
    }
  }, [school, fetchSchool]);

  const displayedSchool = school || fetchedSchool;

  if (loading) {
    return <div>Chargement...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (!displayedSchool) {
    return <div>École non trouvée</div>;
  }

  return (
    <MainLayout title={`${displayedSchool.name} | e-anatra`}>
      <div className="container mx-auto p-10 mt-20 md:mt-28">
        <Image src={displayedSchool.logo_url} alt={displayedSchool.name} width={100} height={100} className="w-32 h-32 object-contain mx-auto mb-4" />
        <h1 className="text-4xl font-bold mb-4">{displayedSchool.name}</h1>
        <p className="text-lg mb-4">{displayedSchool.slogan}</p>
        <p className="text-sm">{displayedSchool.address}</p>
      </div>
    </MainLayout>
  );
};

export const getServerSideProps: GetServerSideProps = async (context) => {
  const { schoolDomain } = context.params!;
  
  const upperCaseDomain = schoolDomain?.toString().toUpperCase();
  if (!upperCaseDomain) {
    return { notFound: true };
  }

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api';
  const response = await fetch(`${API_URL}/schools/${upperCaseDomain}/details/`);
  
  if (!response.ok) { // If the API call was unsuccessful
    return { notFound: true };
  }

  const school = await response.json();

  return {
    props: {
      school,
      schoolDomain: upperCaseDomain,
    },
  };
};


export default SchoolPage;