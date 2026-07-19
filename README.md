# Directrices de Diseño y Arquitectura para Aplicación de Gestión de Huerto Urbano

---

## 1. Objetivo

Desarrollar una aplicación web para la gestión óptima de un huerto urbano, centrada en la planificación de tareas, seguimiento de cultivos, riego, clima (vía AEMET), y registro de acciones. La aplicación debe ser modular, escalable y fácil de mantener.

---

## 2. Arquitectura General

### 2.1. Tipo de Aplicación

- **Aplicación web** (frontend + backend).
- **Monolítica** (inicialmente), con posibilidad de migrar a microservicios si escala.

### 2.2. Componentes Principales

#### Frontend

- **Framework**: React.js (con TypeScript) o Vue.js.
- **UI**: Diseño minimalista y funcional, con dashboard como página principal.
- **Librerías clave**:
  - Chart.js o D3.js para gráficos de rendimiento.
  - FullCalendar o similar para calendarios de tareas.
  - Notistack o SweetAlert para notificaciones.

#### Backend

- **Lenguaje**: Python (Django o FastAPI) o Node.js (Express).
- **API**: RESTful API para comunicación frontend-backend.
- **Autenticación**: JWT (JSON Web Tokens) para gestión de usuarios (si se implementa multi-usuario).

#### Base de Datos

- **Sistema**: PostgreSQL (relacional) o MongoDB (NoSQL si se prioriza flexibilidad en datos no estructurados).
- **Almacenamiento de imágenes**: Sistema de ficheros local o cloud (ej: AWS S3).

#### Integración Externa

- **API de AEMET**: Consulta de datos climáticos (temperatura, humedad, precipitaciones, **viento**) en tiempo real y previsión para el municipio del huerto.
  - Endpoint principal: `https://opendata.aemet.es/opendata/api/` (requiere clave API).
  - Datos a extraer:
    - Temperatura mínima/máxima.
    - Humedad relativa.
    - Precipitación acumulada.
    - Velocidad y dirección del viento (para alertas).
    - Radiación solar (opcional).
  - Frecuencia de actualización: Cada 6-12 horas (o bajo demanda).

---

## 3. Módulos y Funcionalidades

### 3.1. Módulo de Dashboard

- **Objetivo**: Vista central con resumen de tareas, alertas y estado general del huerto.
- **Componentes**:
  - Lista de tareas pendientes por cajón (ordenadas por prioridad/fecha).
  - Alertas urgentes (ej: "Cajón 2: Humedad &lt; 30%", "Viento fuerte: protege los tomates").
  - Resumen climático actual (datos de AEMET) y previsión para 3 días.
  - Gráfico rápido de rendimiento (ej: cosechas de la semana).

### 3.2. Módulo de Gestión de Cajones

- **CRUD de cajones**:
  - Campos: ID, nombre, tipo (cuadrado/redondo/mesa de cultivo), dimensiones (largo/ancho/altura o diámetro), sustrato, ubicación (ej: "Balcón - Sol"), exposición solar (horas de sol directo/indirecto).
  - Asignación temporal de cultivos a cajones (con fechas de inicio/fin).
- **Validaciones**:
  - Dimensiones mínimas para cada tipo de cultivo.
  - Compatibilidad de sustrato con el cultivo seleccionado.

### 3.3. Módulo de Cultivos

- **Base de datos de cultivos**:
  - Campos por cultivo: ID, nombre, familia botánica, fases fenológicas (con duraciones), requisitos (agua, luz, temperatura, pH), profundidad de siembra, distancia entre plantas, método de siembra, indicadores de cosecha.
  - **Fases fenológicas**: Germinación, crecimiento vegetativo, floración, fructificación, maduración, senescencia.
  - **Calendario**: Fechas óptimas de siembra/trasplante/cosecha por municipio (usando datos climáticos históricos de AEMET).
- **Asociaciones y rotaciones**:
  - Matriz de compatibilidad entre cultivos (ej: +1 para asociaciones beneficiosas, -1 para antagonistas).
  - Recomendaciones de rotación por familia botánica (ej: "No plantar solanáceas después de solanáceas").

### 3.4. Módulo de Riego y Fertirrigación

- **Configuración de riego**:
  - Parámetros por cajón: Frecuencia (días/semana), duración (minutos), caudal (L/min), método (goteo, aspersión).
  - Recomendaciones automáticas basadas en:
    - Cultivo asignado y fase fenológica.
    - Datos climáticos (temperatura, viento, humedad).
    - Tipo de sustrato y drenaje del cajón.
- **Historial**: Registro de riegos realizados (fecha, cantidad de agua, método).
- **Alertas**:
  - "Déficit de agua en cajón X" (si humedad del suelo &lt; umbral).
  - "Exceso de riego en cajón Y" (si humedad &gt; umbral).

### 3.5. Módulo de Clima (AEMET)

- **Datos a mostrar**:
  - Temperatura actual/mínima/máxima (°C).
  - Humedad relativa (%).
  - Precipitación acumulada (mm).
  - **Viento**: Velocidad (km/h) y dirección (para alertas de daño en plantas).
  - Radiación solar (opcional, W/m²).
- **Alertas automáticas**:
  - Heladas (temperatura &lt; 0°C).
  - Ola de calor (temperatura &gt; 35°C).
  - Viento fuerte (velocidad &gt; 50 km/h).
  - Lluvias intensas (precipitación &gt; 20 mm en 1 hora).
- **Integración**:
  - Llamadas a la API de AEMET cada 12 horas para actualizar datos.
  - Cacheo de datos para evitar límites de rate de la API.

### 3.6. Módulo de Plagas y Enfermedades

- **Base de datos**:
  - Campos: ID, nombre, síntomas, causas, soluciones (tratar con productos ecológicos), imágenes de referencia.
  - Clasificación por tipo: Hongos, bacterias, insectos, deficiencias nutricionales.
- **Registro de incidencias**:
  - Asociado a cajón y cultivo.
  - Campos: Fecha, tipo de plaga/enfermedad, gravedad, acciones tomadas.
- **Recomendaciones**:
  - Tratamientos preventivos (ej: "Aplicar purín de ortiga cada 15 días").
  - Productos ecológicos recomendados (ej: jabón potásico, bacillus thuringiensis).

### 3.7. Módulo de Diario de Acciones

- **Registro de acciones**:
  - Tipos: Siembra, trasplante, poda, tutorado, aclareo, cosecha, abonado, tratamiento fitosanitario.
  - Campos: ID, cajón, cultivo, tipo de acción, fecha, notas, imágenes (opcional).
- **Navegación**:
  - Filtros por cultivo, cajón, tipo de acción o rango de fechas.
  - Búsqueda por texto libre en notas.

### 3.8. Módulo de Rendimiento y Análisis

- **Registro de cosechas**:
  - Campos: ID, cajón, cultivo, fecha, peso (kg), cantidad (unidades), notas.
- **Gráficos**:
  - Producción por cultivo (kg/m²).
  - Producción por temporada.
  - Consumo de agua por kg de producto cosechado.
- **Análisis de eficiencia**:
  - Coste por cajón (sustrato, semillas, agua) vs. producción.

### 3.9. Módulo de Automatización

- **Notificaciones**:
  - Correo electrónico o notificaciones en app para tareas urgentes.
  - Ejemplos: "Regar cajón 3", "Poda de tomates en 2 días", "Alerta: Viento fuerte previsto mañana".
- **Integración con sensores**:
  - Opcional: Conexión con sensores IoT (ej: ESP32 + sensores de humedad) para automatizar alertas de riego.

### 3.10. Módulo de Configuración

- **Perfil del huerto**:
  - Municipio (para datos de AEMET).
  - Tipo de huerto (urbano, balcón, terraza).
  - Método de cultivo (ecológico, convencional).
- **Preferencias del usuario**:
  - Nivel de experiencia (principiante/avanzado).
  - Umbrales para alertas (ej: humedad mínima del suelo = 30%).

---

## 4. Base de Datos

### 4.1. Esquema Relacional (PostgreSQL)

```sql
-- Ejemplo de tablas principales

-- Usuarios (opcional, si multi-usuario)
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    contrasena_hash VARCHAR(255)
);

-- Huerto
CREATE TABLE huerto (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    municipio VARCHAR(100) NOT NULL,  -- Para API de AEMET
    tipo VARCHAR(50),  -- urbano, balcón, terraza
    metodo_cultivo VARCHAR(50)  -- ecológico, convencional
);

-- Cajones
CREATE TABLE cajones (
    id SERIAL PRIMARY KEY,
    huerto_id INTEGER REFERENCES huerto(id),
    nombre VARCHAR(100),
    tipo VARCHAR(20),  -- cuadrado, redondo, mesa
    largo DECIMAL(5,2),  -- cm (NULL si redondo)
    ancho DECIMAL(5,2),  -- cm (NULL si redondo)
    diametro DECIMAL(5,2),  -- cm (NULL si cuadrado)
    altura DECIMAL(5,2),  -- cm
    sustrato VARCHAR(100),
    ubicacion VARCHAR(100),  -- ej: "Balcón - Sol"
    exposicion_solar INTEGER,  -- horas de sol directo
    tiene_drenaje BOOLEAN DEFAULT TRUE
);

-- Cultivos
CREATE TABLE cultivos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    familia_botanica VARCHAR(100),
    descripcion TEXT,
    requisitos_luz VARCHAR(100),  -- ej: "Sol directo 6-8h"
    requisitos_agua VARCHAR(100),  -- ej: "Riego frecuente"
    temperatura_optima_min DECIMAL(3,1),  -- °C
    temperatura_optima_max DECIMAL(3,1),  -- °C
    ph_optimo_min DECIMAL(3,1),
    ph_optimo_max DECIMAL(3,1)
);

-- Fases Fenológicas
CREATE TABLE fases_fenologicas (
    id SERIAL PRIMARY KEY,
    cultivo_id INTEGER REFERENCES cultivos(id),
    nombre VARCHAR(50) NOT NULL,  -- germinación, crecimiento, etc.
    duracion_dias INTEGER,  -- Duración media en días
    descripcion TEXT,
    recomendaciones TEXT
);

-- Asignación de Cultivos a Cajones
CREATE TABLE asignacion_cultivos (
    id SERIAL PRIMARY KEY,
    cajon_id INTEGER REFERENCES cajones(id),
    cultivo_id INTEGER REFERENCES cultivos(id),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    notas TEXT
);

-- Tareas
CREATE TABLE tareas (
    id SERIAL PRIMARY KEY,
    cajon_id INTEGER REFERENCES cajones(id),
    cultivo_id INTEGER REFERENCES cultivos(id),
    tipo VARCHAR(50) NOT NULL,  -- riego, poda, cosecha, etc.
    fecha_limite DATE,
    estado VARCHAR(20) DEFAULT 'pendiente',  -- pendiente/completada
    prioridad INTEGER,  -- 1-5 (5 = máxima)
    descripcion TEXT
);

-- Diario de Acciones
CREATE TABLE diario (
    id SERIAL PRIMARY KEY,
    cajon_id INTEGER REFERENCES cajones(id),
    cultivo_id INTEGER REFERENCES cultivos(id),
    tipo_accion VARCHAR(50) NOT NULL,  -- siembra, riego, etc.
    fecha TIMESTAMP NOT NULL,
    notas TEXT,
    imagen_url VARCHAR(255)  -- URL a imagen subida
);

-- Cosechas
CREATE TABLE cosechas (
    id SERIAL PRIMARY KEY,
    cajon_id INTEGER REFERENCES cajones(id),
    cultivo_id INTEGER REFERENCES cultivos(id),
    fecha DATE NOT NULL,
    peso_kg DECIMAL(6,2),
    cantidad_unidades INTEGER,
    notas TEXT
);

-- Clima (datos de AEMET)
CREATE TABLE clima (
    id SERIAL PRIMARY KEY,
    huerto_id INTEGER REFERENCES huerto(id),
    fecha DATE NOT NULL,
    temperatura_min DECIMAL(4,1),  -- °C
    temperatura_max DECIMAL(4,1),  -- °C
    humedad_relativa DECIMAL(4,1),  -- %
    precipitacion DECIMAL(6,2),  -- mm
    velocidad_viento DECIMAL(5,1),  -- km/h
    direccion_viento VARCHAR(20),  -- ej: "N", "NE"
    radiacion_solar DECIMAL(6,2)  -- W/m² (opcional)
);

-- Plagas/Enfermedades
CREATE TABLE plagas_enfermedades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),  -- hongo, bacteria, insecto, etc.
    sintomas TEXT,
    causas TEXT,
    soluciones TEXT,
    imagen_url VARCHAR(255)
);

-- Incidencias de Plagas
CREATE TABLE incidencias_plagas (
    id SERIAL PRIMARY KEY,
    cajon_id INTEGER REFERENCES cajones(id),
    cultivo_id INTEGER REFERENCES cultivos(id),
    plaga_id INTEGER REFERENCES plagas_enfermedades(id),
    fecha DATE NOT NULL,
    gravedad VARCHAR(20),  -- leve, moderada, grave
    acciones_tomadas TEXT
);

-- Asociaciones entre Cultivos
CREATE TABLE asociaciones_cultivos (
    id SERIAL PRIMARY KEY,
    cultivo1_id INTEGER REFERENCES cultivos(id),
    cultivo2_id INTEGER REFERENCES cultivos(id),
    tipo_asociacion VARCHAR(20)  -- beneficiosa, antagonista, neutral
);
```

### 4.2. Relaciones Clave

- Un **huerto** tiene múltiples **cajones**. 
- Un **cajón** puede tener múltiples **asignaciones de cultivos** a lo largo del tiempo.
- Un **cultivo** tiene múltiples **fases fenológicas**.
- Las **tareas** y **acciones del diario** se asocian a un **cajón** y/o **cultivo**.
- Las **incidencias de plagas** se registran por **cajón** y **cultivo**.

---

## 5. Flujo de Trabajo

1. **Configuración Inicial**:
  - El usuario define el huerto (municipio, tipo, método de cultivo).
  - Añade cajones con sus características (dimensiones, sustrato, ubicación).
2. **Asignación de Cultivos**:
  - El usuario selecciona cultivos de la base de datos y los asigna a cajones con fechas.
  - La aplicación valida compatibilidad (sustrato, espacio, rotación).
3. **Generación de Tareas Automáticas**:
  - La aplicación genera tareas de riego, poda, cosecha, etc., basadas en:
    - Fases fenológicas del cultivo.
    - Datos climáticos de AEMET (ej: si no ha llovido en 3 días, genera tarea de riego).
    - Alertas de viento o temperatura extrema.
4. **Registro de Acciones**:
  - El usuario registra acciones en el diario (ej: "Regado cajón 1 con 5L de agua").
  - La aplicación actualiza el estado de las tareas.
5. **Seguimiento y Análisis**:
  - El usuario consulta el diario, gráficos de rendimiento y alertas.
  - La aplicación sugiere mejoras (ej: "El cajón 2 tiene bajo rendimiento; considera rotar el cultivo").

---

## 6. Requisitos No Funcionales

- **Rendimiento**:
  - Tiempo de respuesta &lt; 2 segundos para consultas de dashboard.
  - Soportar hasta 100 cajones y 200 cultivos diferentes sin degradación.
- **Seguridad**:
  - Protección contra inyecciones SQL y XSS.
  - Copias de seguridad automáticas de la base de datos (diarias).
- **Escalabilidad**:
  - Diseño modular para añadir nuevos módulos (ej: comercio de semillas).
- **Disponibilidad**:
  - 99% de uptime (excepto mantenimiento programado).

---

## 7. Tecnologías Recomendadas


| Componente        | Tecnología                           |
| ----------------- | ------------------------------------ |
| Frontend          | React.js + TypeScript + Vite         |
| Backend           | FastAPI (Python) o Node.js + Express |
| Base de Datos     | PostgreSQL                           |
| Autenticación     | JWT                                  |
| API Externa       | AEMET (clima)                        |
| Despliegue        | Docker + Nginx (local) o Fly.io      |
| Control Versiones | Git (GitHub/GitLab)                  |


---

## 8. Entregables Esperados

1. **Código fuente** (frontend + backend + scripts de base de datos).
2. **Documentación técnica**:
  - Guía de instalación y despliegue.
  - Diagrama de arquitectura.
  - Diagrama Entidad-Relación de la base de datos.
3. **Base de datos inicial**:
  - Script SQL con tablas y datos de ejemplo (cultivos comunes, fases fenológicas, asociaciones).
4. **Pruebas**:
  - Casos de prueba para módulos críticos (riego, clima, tareas).

---

## 9. Priorización de Desarrollo

1. **Fase 1 (MVP)**:
  - Módulos: Cajones, Cultivos, Dashboard, Tareas, Diario.
  - Integración básica con AEMET (solo temperatura y precipitación).
2. **Fase 2**:
  - Módulos: Riego, Clima (completo con viento), Plagas.
  - Alertas automáticas.
3. **Fase 3**:
  - Módulos: Rendimiento, Análisis, Automatización.
  - Integración con sensores IoT (opcional).

---

## 10. Notas Adicionales

- **Datos de AEMET**:
  - Registrarse en [AEMET OpenData](https://opendata.aemet.es/) para obtener clave API.
  - Usar el endpoint de "Valores climatológicos normales" para datos históricos y "Predicción" para previsión.
  - Ejemplo de llamada para previsión por municipio:
    ```
    https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/{cod_municipio}/
    ```
    (Requiere obtener el código del municipio de la \\\\\\\\\\\\\\\[lista oficial\\\\\\\\\\\\\\\](https://opendata.aemet.es/opendata/sharing/f59c9041b795854170593c62299d9d63)).
- **Viento**:
  - Incluir en alertas: "Viento &gt; 20 km/h: Asegura tutores en tomates y judías".
  - Umbrales configurables por usuario.
- **Pruebas con datos reales**:
  - Usar datos de AEMET de municipios como Madrid, Barcelona o Cádiz para validar el módulo de clima.
