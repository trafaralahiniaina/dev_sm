import React from 'react';
import Image from "next/image";

const Body: React.FC = () => {
  return (
    <div className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-6xl font-bold">Bienvenue sur notre site !</h1>
      <p className="text-2xl">Nous sommes ravis de vous accueillir.</p>
    </div>
  );
};

export default Body;
