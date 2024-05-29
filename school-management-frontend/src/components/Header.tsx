import React from 'react';
import Link from 'next/link';
import { School } from '@/types/school';

interface HeaderProps {
  school: School;
}

const Header: React.FC<HeaderProps> = ({ school }) => {
  const baseUrl = `/${school.website.split('.')[0]}`;

  return (
    <header className="header">
      <nav>
        <Link href={baseUrl}>
          <img src={school.logo_url} alt={school.name} />
        </Link>
        <ul>
          <li>
            <Link href={`${baseUrl}/about`}>
              À propos
            </Link>
          </li>
          <li>
            <Link href={`${baseUrl}/contact`}>
              Contact
            </Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;