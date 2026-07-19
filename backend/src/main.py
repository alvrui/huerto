from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date, datetime
import requests
import os

from . import models, config

# Crear engine de SQLAlchemy
engine = create_engine(config.settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas (solo para desarrollo)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Huerto API", version="0.1.0")


# Dependency para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Models Pydantic (para request/response) ---
class CajonCreate(BaseModel):
    huerto_id: int = Field(..., description="ID del huerto al que pertenece el cajón")
    nombre: str = Field(..., max_length=100, description="Nombre del cajón")
    tipo: str = Field(..., max_length=20, description="Tipo: cuadrado, redondo, mesa")
    largo: Optional[float] = Field(None, description="Largo en cm (solo para tipo cuadrado/mesa)")
    ancho: Optional[float] = Field(None, description="Ancho en cm (solo para tipo cuadrado/mesa)")
    diametro: Optional[float] = Field(None, description="Diámetro en cm (solo para tipo redondo)")
    altura: float = Field(..., description="Altura en cm")
    sustrato: str = Field(..., max_length=100, description="Tipo de sustrato")
    ubicacion: str = Field(..., max_length=100, description="Ubicación física")
    exposicion_solar: int = Field(..., description="Horas de sol directo al día")
    tiene_drenaje: bool = Field(True, description="¿Tiene sistema de drenaje?")


class CajonResponse(BaseModel):
    id: int
    huerto_id: int
    nombre: str
    tipo: str
    largo: Optional[float]
    ancho: Optional[float]
    diametro: Optional[float]
    altura: float
    sustrato: str
    ubicacion: str
    exposicion_solar: int
    tiene_drenaje: bool

    class Config:
        from_attributes = True


class CultivoCreate(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre del cultivo")
    familia_botanica: Optional[str] = Field(None, max_length=100, description="Familia botánica")
    descripcion: Optional[str] = Field(None, description="Descripción detallada")
    requisitos_luz: Optional[str] = Field(None, max_length=100, description="Requisitos de luz")
    requisitos_agua: Optional[str] = Field(None, max_length=100, description="Requisitos de agua")
    temperatura_optima_min: Optional[float] = Field(None, description="Temperatura óptima mínima (°C)")
    temperatura_optima_max: Optional[float] = Field(None, description="Temperatura óptima máxima (°C)")
    ph_optimo_min: Optional[float] = Field(None, description="pH óptimo mínimo")
    ph_optimo_max: Optional[float] = Field(None, description="pH óptimo máximo")


class CultivoResponse(BaseModel):
    id: int
    nombre: str
    familia_botanica: Optional[str]
    descripcion: Optional[str]
    requisitos_luz: Optional[str]
    requisitos_agua: Optional[str]
    temperatura_optima_min: Optional[float]
    temperatura_optima_max: Optional[float]
    ph_optimo_min: Optional[float]
    ph_optimo_max: Optional[float]

    class Config:
        from_attributes = True


class HuertoCreate(BaseModel):
    municipio: str = Field(..., max_length=100, description="Municipio del huerto")
    tipo: Optional[str] = Field(None, max_length=50, description="Tipo: urbano, balcón, terraza")
    metodo_cultivo: Optional[str] = Field(None, max_length=50, description="Método: ecológico, convencional")


class HuertoResponse(BaseModel):
    id: int
    municipio: str
    tipo: Optional[str]
    metodo_cultivo: Optional[str]

    class Config:
        from_attributes = True


class AsignacionCultivoCreate(BaseModel):
    cajon_id: int = Field(..., description="ID del cajón")
    cultivo_id: int = Field(..., description="ID del cultivo")
    fecha_inicio: date = Field(..., description="Fecha de inicio de la asignación")
    fecha_fin: Optional[date] = Field(None, description="Fecha de fin de la asignación")
    notas: Optional[str] = Field(None, description="Notas adicionales")


class AsignacionCultivoResponse(BaseModel):
    id: int
    cajon_id: int
    cultivo_id: int
    fecha_inicio: date
    fecha_fin: Optional[date]
    notas: Optional[str]

    class Config:
        from_attributes = True


class ClimaResponse(BaseModel):
    id: int
    huerto_id: int
    fecha: date
    temperatura_min: float
    temperatura_max: float
    humedad_relativa: float
    precipitacion: float
    velocidad_viento: float
    direccion_viento: str
    radiacion_solar: Optional[float]

    class Config:
        from_attributes = True


class ClimaCreate(BaseModel):
    huerto_id: int = Field(..., description="ID del huerto")
    fecha: date = Field(..., description="Fecha de los datos climáticos")
    temperatura_min: float = Field(..., description="Temperatura mínima (°C)")
    temperatura_max: float = Field(..., description="Temperatura máxima (°C)")
    humedad_relativa: float = Field(..., description="Humedad relativa (%)")
    precipitacion: float = Field(..., description="Precipitación (mm)")
    velocidad_viento: float = Field(..., description="Velocidad del viento (km/h)")
    direccion_viento: str = Field(..., description="Dirección del viento (ej: N, NE)")
    radiacion_solar: Optional[float] = Field(None, description="Radiación solar (W/m²)")


# --- Endpoints Huerto ---
@app.post("/huerto/", response_model=HuertoResponse, status_code=status.HTTP_201_CREATED)
def crear_huerto(huerto: HuertoCreate, db: Session = Depends(get_db)):
    db_huerto = models.Huerto(**huerto.model_dump())
    db.add(db_huerto)
    db.commit()
    db.refresh(db_huerto)
    return db_huerto


@app.get("/huerto/", response_model=List[HuertoResponse])
def listar_huertos(db: Session = Depends(get_db)):
    return db.query(models.Huerto).all()


@app.get("/huerto/{huerto_id}", response_model=HuertoResponse)
def obtener_huerto(huerto_id: int, db: Session = Depends(get_db)):
    huerto = db.query(models.Huerto).filter(models.Huerto.id == huerto_id).first()
    if not huerto:
        raise HTTPException(status_code=404, detail="Huerto no encontrado")
    return huerto


# --- Endpoints Cajones ---
@app.post("/cajones/", response_model=CajonResponse, status_code=status.HTTP_201_CREATED)
def crear_cajon(cajon: CajonCreate, db: Session = Depends(get_db)):
    # Validación: si tipo es cuadrado o mesa, largo y ancho son obligatorios
    if cajon.tipo in ["cuadrado", "mesa"] and (cajon.largo is None or cajon.ancho is None):
        raise HTTPException(
            status_code=400,
            detail="Para tipo 'cuadrado' o 'mesa', largo y ancho son obligatorios"
        )
    # Validación: si tipo es redondo, diametro es obligatorio
    if cajon.tipo == "redondo" and cajon.diametro is None:
        raise HTTPException(
            status_code=400,
            detail="Para tipo 'redondo', diámetro es obligatorio"
        )
    
    db_cajon = models.Cajon(**cajon.model_dump())
    db.add(db_cajon)
    db.commit()
    db.refresh(db_cajon)
    return db_cajon


@app.get("/cajones/", response_model=List[CajonResponse])
def listar_cajones(db: Session = Depends(get_db)):
    return db.query(models.Cajon).all()


@app.get("/cajones/{cajon_id}", response_model=CajonResponse)
def obtener_cajon(cajon_id: int, db: Session = Depends(get_db)):
    cajon = db.query(models.Cajon).filter(models.Cajon.id == cajon_id).first()
    if not cajon:
        raise HTTPException(status_code=404, detail="Cajón no encontrado")
    return cajon


@app.put("/cajones/{cajon_id}", response_model=CajonResponse)
def actualizar_cajon(cajon_id: int, cajon: CajonCreate, db: Session = Depends(get_db)):
    db_cajon = db.query(models.Cajon).filter(models.Cajon.id == cajon_id).first()
    if not db_cajon:
        raise HTTPException(status_code=404, detail="Cajón no encontrado")
    
    # Validaciones (igual que en POST)
    if cajon.tipo in ["cuadrado", "mesa"] and (cajon.largo is None or cajon.ancho is None):
        raise HTTPException(
            status_code=400,
            detail="Para tipo 'cuadrado' o 'mesa', largo y ancho son obligatorios"
        )
    if cajon.tipo == "redondo" and cajon.diametro is None:
        raise HTTPException(
            status_code=400,
            detail="Para tipo 'redondo', diámetro es obligatorio"
        )
    
    for key, value in cajon.model_dump().items():
        setattr(db_cajon, key, value)
    db.commit()
    db.refresh(db_cajon)
    return db_cajon


@app.delete("/cajones/{cajon_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cajon(cajon_id: int, db: Session = Depends(get_db)):
    db_cajon = db.query(models.Cajon).filter(models.Cajon.id == cajon_id).first()
    if not db_cajon:
        raise HTTPException(status_code=404, detail="Cajón no encontrado")
    db.delete(db_cajon)
    db.commit()


# --- Endpoints Cultivos ---
@app.post("/cultivos/", response_model=CultivoResponse, status_code=status.HTTP_201_CREATED)
def crear_cultivo(cultivo: CultivoCreate, db: Session = Depends(get_db)):
    db_cultivo = models.Cultivo(**cultivo.model_dump())
    db.add(db_cultivo)
    db.commit()
    db.refresh(db_cultivo)
    return db_cultivo


@app.get("/cultivos/", response_model=List[CultivoResponse])
def listar_cultivos(db: Session = Depends(get_db)):
    return db.query(models.Cultivo).all()


@app.get("/cultivos/{cultivo_id}", response_model=CultivoResponse)
def obtener_cultivo(cultivo_id: int, db: Session = Depends(get_db)):
    cultivo = db.query(models.Cultivo).filter(models.Cultivo.id == cultivo_id).first()
    if not cultivo:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    return cultivo


# --- Endpoints Asignación Cultivos ---
@app.post("/asignaciones/", response_model=AsignacionCultivoResponse, status_code=status.HTTP_201_CREATED)
def crear_asignacion(asignacion: AsignacionCultivoCreate, db: Session = Depends(get_db)):
    db_asignacion = models.AsignacionCultivo(**asignacion.model_dump())
    db.add(db_asignacion)
    db.commit()
    db.refresh(db_asignacion)
    return db_asignacion


@app.get("/asignaciones/", response_model=List[AsignacionCultivoResponse])
def listar_asignaciones(db: Session = Depends(get_db)):
    return db.query(models.AsignacionCultivo).all()


@app.get("/asignaciones/{asignacion_id}", response_model=AsignacionCultivoResponse)
def obtener_asignacion(asignacion_id: int, db: Session = Depends(get_db)):
    asignacion = db.query(models.AsignacionCultivo).filter(models.AsignacionCultivo.id == asignacion_id).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return asignacion


# --- Endpoints Clima ---
@app.post("/clima/", response_model=ClimaResponse, status_code=status.HTTP_201_CREATED)
def crear_clima(clima: ClimaCreate, db: Session = Depends(get_db)):
    db_clima = models.Clima(**clima.model_dump())
    db.add(db_clima)
    db.commit()
    db.refresh(db_clima)
    return db_clima


@app.get("/clima/", response_model=List[ClimaResponse])
def listar_clima(db: Session = Depends(get_db)):
    return db.query(models.Clima).all()


@app.get("/clima/huerto/{huerto_id}", response_model=List[ClimaResponse])
def listar_clima_por_huerto(huerto_id: int, db: Session = Depends(get_db)):
    return db.query(models.Clima).filter(models.Clima.huerto_id == huerto_id).all()


@app.get("/clima/aemet/{municipio}")
def obtener_clima_aemet(municipio: str):
    """
    Obtiene datos climáticos de AEMET para un municipio.
    Requiere la clave API de AEMET en .env (AEMET_API_KEY).
    """
    # Mapeo de municipios a códigos AEMET (ejemplos)
    # TODO: Ampliar esta lista o usar la API de AEMET para buscar códigos
    codigos_municipios = {
        "madrid": "28079",
        "barcelona": "08019",
        "valencia": "46250",
        "sevilla": "41091",
        "bilbao": "48020",
        "malaga": "29067",
        "zaragoza": "50297",
        "alicante": "03014",
        "cadiz": "11012",
        "coruna": "15030",
    }
    
    # Normalizar el municipio (minúsculas, sin tildes)
    municipio_normalizado = municipio.lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    
    if municipio_normalizado not in codigos_municipios:
        raise HTTPException(
            status_code=400,
            detail=f"Municipio '{municipio}' no soportado. Usa uno de: {list(codigos_municipios.keys())}"
        )
    
    codigo_municipio = codigos_municipios[municipio_normalizado]
    api_key = config.settings.AEMET_API_KEY
    
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Clave API de AEMET no configurada. Añade AEMET_API_KEY a tu .env"
        )
    
    # URL de la API de AEMET para predicción por municipio
    url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/{codigo_municipio}/"
    
    try:
        # Primera llamada para obtener el endpoint real (AEMET usa redirección)
        headers = {"api_key": api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # La respuesta contiene un JSON con el endpoint real
        data = response.json()
        if "datos" not in data:
            raise HTTPException(
                status_code=500,
                detail=f"Error en la respuesta de AEMET: {data}"
            )
        
        # Obtener los datos reales
        datos_url = data["datos"]
        datos_response = requests.get(datos_url)
        datos_response.raise_for_status()
        clima_data = datos_response.json()
        
        # Extraer información relevante (simplificado para el MVP)
        # La estructura de AEMET es compleja, aquí extraemos el primer día
        if "prediccion" not in clima_data or "dia" not in clima_data["prediccion"]:
            raise HTTPException(
                status_code=500,
                detail="Formato de datos de AEMET no esperado"
            )
        
        primer_dia = clima_data["prediccion"]["dia"][0]
        
        # Extraer datos climáticos
        temperatura_min = primer_dia.get("temperatura", {}).get("minima", 0)
        temperatura_max = primer_dia.get("temperatura", {}).get("maxima", 0)
        humedad_relativa = primer_dia.get("humedadRelativa", {}).get("maxima", 0)
        precipitacion = primer_dia.get("precipitacion", [{}])[0].get("value", 0) if isinstance(primer_dia.get("precipitacion"), list) else 0
        velocidad_viento = primer_dia.get("viento", [{}])[0].get("velocidad", 0) if isinstance(primer_dia.get("viento"), list) else 0
        direccion_viento = primer_dia.get("viento", [{}])[0].get("direccion", "N") if isinstance(primer_dia.get("viento"), list) else "N"
        
        return {
            "municipio": municipio,
            "fecha": primer_dia.get("fecha", ""),
            "temperatura_min": temperatura_min,
            "temperatura_max": temperatura_max,
            "humedad_relativa": humedad_relativa,
            "precipitacion": precipitacion,
            "velocidad_viento": velocidad_viento,
            "direccion_viento": direccion_viento,
            "fuente": "AEMET"
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al conectar con AEMET: {str(e)}"
        )
