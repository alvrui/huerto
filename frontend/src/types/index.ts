// Tipos para Huerto
export interface Huerto {
  id: number;
  municipio: string;
  tipo?: string;
  metodo_cultivo?: string;
}

// Tipos para Cajón
export interface Cajon {
  id: number;
  huerto_id: number;
  nombre: string;
  tipo: string;
  largo?: number | null;
  ancho?: number | null;
  diametro?: number | null;
  altura: number;
  sustrato: string;
  ubicacion: string;
  exposicion_solar: number;
  tiene_drenaje: boolean;
}

// Tipos para Cultivo
export interface Cultivo {
  id: number;
  nombre: string;
  familia_botanica?: string;
  descripcion?: string;
  requisitos_luz?: string;
  requisitos_agua?: string;
  temperatura_optima_min?: number;
  temperatura_optima_max?: number;
  ph_optimo_min?: number;
  ph_optimo_max?: number;
}

// Tipos para Asignación de Cultivos
export interface AsignacionCultivo {
  id: number;
  cajon_id: number;
  cultivo_id: number;
  fecha_inicio: string; // ISO date string
  fecha_fin?: string | null;
  notas?: string;
}

// Tipos para Clima (AEMET)
export interface Clima {
  id: number;
  huerto_id: number;
  fecha: string; // ISO date string
  temperatura_min: number;
  temperatura_max: number;
  humedad_relativa: number;
  precipitacion: number;
  velocidad_viento: number;
  direccion_viento: string;
  radiacion_solar?: number;
}

// Tipos para respuestas de la API
export interface ApiResponse<T> {
  data?: T;
  message?: string;
  error?: string;
}

// Tipos para formularios
export interface HuertoFormData {
  municipio: string;
  tipo?: string;
  metodo_cultivo?: string;
}

export interface CajonFormData {
  huerto_id: number;
  nombre: string;
  tipo: string;
  largo?: number | null;
  ancho?: number | null;
  diametro?: number | null;
  altura: number;
  sustrato: string;
  ubicacion: string;
  exposicion_solar: number;
  tiene_drenaje: boolean;
}

export interface CultivoFormData {
  nombre: string;
  familia_botanica?: string;
  descripcion?: string;
  requisitos_luz?: string;
  requisitos_agua?: string;
  temperatura_optima_min?: number;
  temperatura_optima_max?: number;
  ph_optimo_min?: number;
  ph_optimo_max?: number;
}

export interface AsignacionCultivoFormData {
  cajon_id: number;
  cultivo_id: number;
  fecha_inicio: string;
  fecha_fin?: string;
  notas?: string;
}
