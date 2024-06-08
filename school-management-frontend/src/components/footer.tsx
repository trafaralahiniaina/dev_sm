import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-zinc-800 text-white py-4">
      <div className="container mx-auto text-center">
        <p>&copy; {new Date().getFullYear()} Mon Site. Tous droits réservés.</p>
      </div>
    </footer>
  );
};

export default Footer;
