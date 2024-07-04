// src/components/main/SchoolCard.tsx

import Image from 'next/image';
import Link from 'next/link';
import { School } from '../../types';

interface SchoolCardProps {
  school: School;
  onEdit?: () => void;
  onDelete?: () => void;
}

export default function SchoolCard({ school, onEdit, onDelete }: SchoolCardProps) {
  return (
    <div className="border rounded-lg shadow-lg p-4">
      <Image src={school.logo_url} alt={school.name} width={100} height={100} className="mx-auto" />
      <h2 className="text-xl font-bold mt-2">{school.name}</h2>
      <p className="text-sm text-gray-600">{school.slogan}</p>
      <p className="mt-2">{school.address}</p>
      <Link
          href={`http://${school.sigle.toLowerCase()}.${window.location.hostname}:${window.location.port}`}
          className="text-blue-500 hover:underline mt-2 block"
        >
          Visiter le site
      </Link>
      {onEdit && (
        <button onClick={onEdit} className="mt-2 mr-2 px-3 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600">
          Modifier
        </button>
      )}
      {onDelete && (
        <button onClick={onDelete} className="mt-2 px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600">
          Supprimer
        </button>
      )}
    </div>
  );
}