import React from 'react';
import { School } from '@/types/school';

interface FooterProps {
  school: School;
}

const Footer: React.FC<FooterProps> = ({ school }) => {
  return (
    <footer className="footer">
      <p>&copy; {new Date().getFullYear()} {school.name}. Tous droits réservés.</p>
    </footer>
  );
};

export default Footer;