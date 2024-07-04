// src/components/main/SchoolList.tsx

import { School } from '../../types';
import SchoolCard from './SchoolCard';

interface SchoolListProps {
  schools: School[];
  onEdit?: (school: School) => void;
  onDelete?: (id: number) => void;
}

export default function SchoolList({ schools, onEdit, onDelete }: SchoolListProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {schools.map((school) => (
        <SchoolCard 
          key={school.id} 
          school={school} 
          onEdit={onEdit ? () => onEdit(school) : undefined}
          onDelete={onDelete ? () => onDelete(school.id) : undefined}
        />
      ))}
    </div>
  );
}