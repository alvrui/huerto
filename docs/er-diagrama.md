# Diagrama Entidad-Relación

```mermaid
erDiagram
    HUERTO ||--o{ CAJONES : contiene
    HUERTO ||--o{ CLIMA : registra
    CAJONES ||--o{ ASIGNACION_CULTIVOS : asigna
    CULTIVOS ||--o{ ASIGNACION_CULTIVOS : se_asigna_a
    CULTIVOS ||--o{ FASES_FENOLOGICAS : tiene
    CULTIVOS ||--o{ ASOCIACIONES_CULTIVOS : se_asocia_con
    CAJONES ||--o{ TAREAS : genera
    CULTIVOS ||--o{ TAREAS : requiere
    CAJONES ||--o{ DIARIO : registra
    CULTIVOS ||--o{ DIARIO : afecta_a
    CAJONES ||--o{ COSECHAS : produce
    CULTIVOS ||--o{ COSECHAS : es
    CAJONES ||--o{ INCIDENCIAS_PLAGAS : reporta
    CULTIVOS ||--o{ INCIDENCIAS_PLAGAS : afecta_a
    PLAGAS_ENFERMEDADES ||--o{ INCIDENCIAS_PLAGAS : es

    HUERTO {
        int id PK
        string municipio
        string tipo
        string metodo_cultivo
    }

    CAJONES {
        int id PK
        int huerto_id FK
        string nombre
        string tipo
        decimal largo
        decimal ancho
        decimal diametro
        decimal altura
        string sustrato
        string ubicacion
        int exposicion_solar
        boolean tiene_drenaje
    }

    CULTIVOS {
        int id PK
        string nombre
        string familia_botanica
        string descripcion
        string requisitos_luz
        string requisitos_agua
        decimal temperatura_optima_min
        decimal temperatura_optima_max
        decimal ph_optimo_min
        decimal ph_optimo_max
    }

    FASES_FENOLOGICAS {
        int id PK
        int cultivo_id FK
        string nombre
        int duracion_dias
        string descripcion
        string recomendaciones
    }

    ASIGNACION_CULTIVOS {
        int id PK
        int cajon_id FK
        int cultivo_id FK
        date fecha_inicio
        date fecha_fin
        string notas
    }

    TAREAS {
        int id PK
        int cajon_id FK
        int cultivo_id FK
        string tipo
        date fecha_limite
        string estado
        int prioridad
        string descripcion
    }

    DIARIO {
        int id PK
        int cajon_id FK
        int cultivo_id FK
        string tipo_accion
        timestamp fecha
        string notas
        string imagen_url
    }

    COSECHAS {
        int id PK
        int cajon_id FK
        int cultivo_id FK
        date fecha
        decimal peso_kg
        int cantidad_unidades
        string notas
    }

    CLIMA {
        int id PK
        int huerto_id FK
        date fecha
        decimal temperatura_min
        decimal temperatura_max
        decimal humedad_relativa
        decimal precipitacion
        decimal velocidad_viento
        string direccion_viento
        decimal radiacion_solar
    }

    PLAGAS_ENFERMEDADES {
        int id PK
        string nombre
        string tipo
        string sintomas
        string causas
        string soluciones
        string imagen_url
    }

    INCIDENCIAS_PLAGAS {
        int id PK
        int cajon_id FK
        int cultivo_id FK
        int plaga_id FK
        date fecha
        string gravedad
        string acciones_tomadas
    }

    ASOCIACIONES_CULTIVOS {
        int id PK
        int cultivo1_id FK
        int cultivo2_id FK
        string tipo_asociacion
    }
```

## Notas
- **Relaciones**:
  - Un **Huerto** tiene múltiples **Cajones**. 
  - Un **Cajón** puede tener múltiples **Asignaciones de Cultivos** a lo largo del tiempo.
  - Un **Cultivo** tiene múltiples **Fases Fenológicas**.
  - Las **Tareas** y **Acciones del Diario** se asocian a un **Cajón** y/o **Cultivo**. 
  - Las **Incidencias de Plagas** se registran por **Cajón** y **Cultivo**. 

- **Tablas implementadas en el MVP**:
  - `HUERTO`, `CAJONES`, `CULTIVOS`, `ASIGNACION_CULTIVOS`.
- **Tablas pendientes para futuras fases**:
  - `FASES_FENOLOGICAS`, `TAREAS`, `DIARIO`, `COSECHAS`, `CLIMA`, `PLAGAS_ENFERMEDADES`, `INCIDENCIAS_PLAGAS`, `ASOCIACIONES_CULTIVOS`.
