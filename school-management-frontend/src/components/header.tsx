import React from 'react';
import Link from 'next/link';
import Image from "next/image";

const Header: React.FC = () => {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-gray-800 text-white">
      <div className="container mx-auto flex justify-between items-center py-4 px-8">
        <div className="flex items-center">
          <div className="w-10 h-10 bg-white rounded-full mr-4"></div>
          <h1 className="text-2xl font-bold">Mon Site</h1>
        </div>
        <nav>
          <ul className="flex space-x-4">
            <li>
              <Link href="/">
                <span className="hover:text-gray-300">Accueil</span>
              </Link>
            </li>
            <li>
              <Link href="/about">
                <span className="hover:text-gray-300">À propos</span>
              </Link>
            </li>
            <li>
              <Link href="/contact">
                <span className="hover:text-gray-300">Contact</span>
              </Link>
            </li>
            <li>
              <Link href="/login">
                <span className="hover:text-gray-300">Connexion</span>
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
