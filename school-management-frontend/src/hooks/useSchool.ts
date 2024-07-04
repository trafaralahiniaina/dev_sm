// src\hooks\useSchool.ts

import { useState, useCallback, useEffect } from 'react';
import { School } from '../types';
import {
  fetchSchools as apiFetchSchools,
  createSchool as apiCreateSchool,
  updateSchool as apiUpdateSchool,
  deleteSchool as apiDeleteSchool,
  fetchSchoolBySigle
} from '../lib/api';

export function useSchools() {
  const [schools, setSchools] = useState<School[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSchools = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetchSchools();
      setSchools(data);
    } catch (error) {
      setError('Erreur lors de la récupération des écoles');
      console.error('Erreur lors de la récupération des écoles:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  const createSchool = useCallback(async (schoolData: Partial<School>) => {
    setLoading(true);
    setError(null);
    try {
      const newSchool = await apiCreateSchool(schoolData);
      setSchools(prevSchools => [...prevSchools, newSchool]);
      return newSchool;
    } catch (error) {
      setError("Erreur lors de la création de l'école");
      console.error("Erreur lors de la création de l'école:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  const updateSchool = useCallback(async (id: number, schoolData: Partial<School>) => {
    setLoading(true);
    setError(null);
    try {
      const updatedSchool = await apiUpdateSchool(id, schoolData);
      setSchools(prevSchools => prevSchools.map(school => (school.id === id ? updatedSchool : school)));
      return updatedSchool;
    } catch (error) {
      setError("Erreur lors de la mise à jour de l'école");
      console.error("Erreur lors de la mise à jour de l'école:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteSchool = useCallback(async (id: number) => {
    setLoading(true);
    setError(null);
    try {
      await apiDeleteSchool(id);
      setSchools(prevSchools => prevSchools.filter(school => school.id !== id));
    } catch (error) {
      setError("Erreur lors de la suppression de l'école");
      console.error("Erreur lors de la suppression de l'école:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  return { schools, loading, error, fetchSchools, createSchool, updateSchool, deleteSchool };
}

export const useSchool = (sigle: string) => {
  const [school, setSchool] = useState<School | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchSchool = useCallback(async () => {
    if (sigle !== 'localhost:3000') {
      setLoading(true);
      setError(null);
      try {
        const schoolData = await fetchSchoolBySigle(sigle);
        setSchool(schoolData);
        if (!schoolData) {
          setError("École non trouvée");
        }
      } catch (error) {
        setError("Erreur lors du chargement de l'école");
        console.error('Erreur lors du chargement de l\'école ${sigle}:, error');
      } finally {
        setLoading(false);
      }
    }
  }, [sigle]);

  useEffect(() => {
    fetchSchool();
  }, [fetchSchool]);

  return { school, error, loading, fetchSchool };
};