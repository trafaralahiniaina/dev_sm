import React from 'react';
import Image from "next/image";

const Index: React.FC = () => {
  return (
      <div className="flex min-h-screen flex-col items-center justify-between p-10 mt-20 md:mt-28">
        <h1 className="text-6xl font-bold">Bienvenue sur notre site !</h1>
        <p className="text-2xl">Nous sommes ravis de vous accueillir.</p>
      </div>
  );
};

export default Index;
