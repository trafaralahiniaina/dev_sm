// utils/fetchSchoolData.ts
import axios from 'axios';
import { School } from '@/types/school';

export const fetchSchoolData = async (schoolDomain: string): Promise<School | null> => {
  try {
    const response = await axios.get(`/api/schools/data?domain=${schoolDomain}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching school data:', error);
    return null;
  }
};