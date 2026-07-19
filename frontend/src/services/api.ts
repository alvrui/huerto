import axios from 'axios';

// Configuración base de Axios
const api = axios.create({
  baseURL: '/api', // Proxy configurado en vite.config.ts
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- Endpoints de Huerto ---
export const huertoApi = {
  create: (data: Omit<Huerto, 'id'>) => api.post<Huerto>('/huerto/', data),
  getAll: () => api.get<Huerto[]>('/huerto/'),
  getById: (id: number) => api.get<Huerto>(`/huerto/${id}`),
};

// --- Endpoints de Cajones ---
export const cajonApi = {
  create: (data: Omit<Cajon, 'id'>) => api.post<Cajon>('/cajones/', data),
  getAll: () => api.get<Cajon[]>('/cajones/'),
  getById: (id: number) => api.get<Cajon>(`/cajones/${id}`),
  update: (id: number, data: Partial<Omit<Cajon, 'id'>>) => 
    api.put<Cajon>(`/cajones/${id}`, data),
  delete: (id: number) => api.delete(`/cajones/${id}`),
};

// --- Endpoints de Cultivos ---
export const cultivoApi = {
  create: (data: Omit<Cultivo, 'id'>) => api.post<Cultivo>('/cultivos/', data),
  getAll: () => api.get<Cultivo[]>('/cultivos/'),
  getById: (id: number) => api.get<Cultivo>(`/cultivos/${id}`),
};

// --- Endpoints de Asignaciones ---
export const asignacionApi = {
  create: (data: Omit<AsignacionCultivo, 'id'>) => 
    api.post<AsignacionCultivo>('/asignaciones/', data),
  getAll: () => api.get<AsignacionCultivo[]>('/asignaciones/'),
  getById: (id: number) => api.get<AsignacionCultivo>(`/asignaciones/${id}`),
};

// --- Endpoints de Clima ---
export const climaApi = {
  getAll: () => api.get<Clima[]>('/clima/'),
  getByHuertoId: (huertoId: number) => api.get<Clima[]>(`/clima/huerto/${huertoId}`),
  getAEMET: (municipio: string) => api.get(`/clima/aemet/${municipio}`),
};

// Tipos importados para TypeScript
import type {
  Huerto,
  Cajon,
  Cultivo,
  AsignacionCultivo,
  Clima,
} from '../types';

export default api;
