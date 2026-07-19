from sqlalchemy import Column, Integer, String, Decimal, Boolean, Date, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Huerto(Base):
    __tablename__ = "huerto"
    id = Column(Integer, primary_key=True, index=True)
    municipio = Column(String(100), nullable=False)
    tipo = Column(String(50))  # urbano, balcón, terraza
    metodo_cultivo = Column(String(50))  # ecológico, convencional


class Cajon(Base):
    __tablename__ = "cajones"
    id = Column(Integer, primary_key=True, index=True)
    huerto_id = Column(Integer, ForeignKey("huerto.id"), nullable=False)
    nombre = Column(String(100))
    tipo = Column(String(20))  # cuadrado, redondo, mesa
    largo = Column(Decimal(5, 2))  # cm
    ancho = Column(Decimal(5, 2))  # cm
    diametro = Column(Decimal(5, 2))  # cm
    altura = Column(Decimal(5, 2))  # cm
    sustrato = Column(String(100))
    ubicacion = Column(String(100))  # ej: "Balcón - Sol"
    exposicion_solar = Column(Integer)  # horas de sol directo
    tiene_drenaje = Column(Boolean, default=True)

    huerto = relationship("Huerto", backref="cajones")


class Cultivo(Base):
    __tablename__ = "cultivos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    familia_botanica = Column(String(100))
    descripcion = Column(Text)
    requisitos_luz = Column(String(100))  # ej: "Sol directo 6-8h"
    requisitos_agua = Column(String(100))  # ej: "Riego frecuente"
    temperatura_optima_min = Column(Decimal(3, 1))  # °C
    temperatura_optima_max = Column(Decimal(3, 1))  # °C
    ph_optimo_min = Column(Decimal(3, 1))
    ph_optimo_max = Column(Decimal(3, 1))


class AsignacionCultivo(Base):
    __tablename__ = "asignacion_cultivos"
    id = Column(Integer, primary_key=True, index=True)
    cajon_id = Column(Integer, ForeignKey("cajones.id"), nullable=False)
    cultivo_id = Column(Integer, ForeignKey("cultivos.id"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    notas = Column(Text)

    cajon = relationship("Cajon", backref="asignaciones")
    cultivo = relationship("Cultivo", backref="asignaciones")
