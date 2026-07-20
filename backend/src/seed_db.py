"""
Script para cargar datos iniciales en la base de datos.
Se ejecuta al iniciar el backend si no hay datos.
"""
from sqlalchemy.orm import Session
from . import models
from datetime import date


def seed_database(db: Session):
    """Carga datos iniciales si la base de datos está vacía."""
    
    # Verificar si ya hay datos
    if db.query(models.Huerto).first():
        print("La base de datos ya tiene datos. No se cargan datos iniciales.")
        return
    
    # Crear un huerto de ejemplo
    huerto = models.Huerto(
        municipio="Madrid",
        tipo="urbano",
        metodo_cultivo="ecológico"
    )
    db.add(huerto)
    db.commit()
    db.refresh(huerto)
    
    # Crear cajones de ejemplo
    cajones = [
        models.Cajon(
            huerto_id=huerto.id,
            nombre="Cajón 1",
            tipo="cuadrado",
            largo=50.0,
            ancho=30.0,
            altura=20.0,
            sustrato="Tierra con compost",
            ubicacion="Balcón - Sol",
            exposicion_solar=6,
            tiene_drenaje=True
        ),
        models.Cajon(
            huerto_id=huerto.id,
            nombre="Cajón 2",
            tipo="redondo",
            diametro=40.0,
            altura=25.0,
            sustrato="Sustrato universal",
            ubicacion="Balcón - Sombra",
            exposicion_solar=4,
            tiene_drenaje=True
        ),
        models.Cajon(
            huerto_id=huerto.id,
            nombre="Mesa de cultivo",
            tipo="mesa",
            largo=80.0,
            ancho=40.0,
            altura=15.0,
            sustrato="Fibra de coco",
            ubicacion="Terraza",
            exposicion_solar=8,
            tiene_drenaje=True
        )
    ]
    db.add_all(cajones)
    db.commit()
    
    # Crear cultivos de ejemplo
    cultivos = [
        models.Cultivo(
            nombre="Tomate",
            familia_botanica="Solanáceas",
            descripcion="Planta anual de clima cálido. Requiere tutores.",
            requisitos_luz="Sol directo 6-8h",
            requisitos_agua="Riego frecuente",
            temperatura_optima_min=15.0,
            temperatura_optima_max=30.0,
            ph_optimo_min=6.0,
            ph_optimo_max=7.0
        ),
        models.Cultivo(
            nombre="Lechuga",
            familia_botanica="Asteráceas",
            descripcion="Hortaliza de hoja verde. Crece rápido en clima fresco.",
            requisitos_luz="Sol directo o semisombra",
            requisitos_agua="Riego constante",
            temperatura_optima_min=10.0,
            temperatura_optima_max=25.0,
            ph_optimo_min=6.0,
            ph_optimo_max=7.0
        ),
        models.Cultivo(
            nombre="Zanahoria",
            familia_botanica="Apiáceas",
            descripcion="Raíz comestible. Requiere suelo suelto y profundo.",
            requisitos_luz="Sol directo",
            requisitos_agua="Riego moderado",
            temperatura_optima_min=15.0,
            temperatura_optima_max=25.0,
            ph_optimo_min=6.0,
            ph_optimo_max=7.5
        ),
        models.Cultivo(
            nombre="Pimiento",
            familia_botanica="Solanáceas",
            descripcion="Planta de clima cálido. Variedades dulces y picantes.",
            requisitos_luz="Sol directo 6-8h",
            requisitos_agua="Riego regular",
            temperatura_optima_min=20.0,
            temperatura_optima_max=30.0,
            ph_optimo_min=6.0,
            ph_optimo_max=7.0
        ),
        models.Cultivo(
            nombre="Albahaca",
            familia_botanica="Lamiáceas",
            descripcion="Planta aromática. Ideal para macetas.",
            requisitos_luz="Sol directo o semisombra",
            requisitos_agua="Riego frecuente",
            temperatura_optima_min=20.0,
            temperatura_optima_max=30.0,
            ph_optimo_min=6.0,
            ph_optimo_max=7.5
        )
    ]
    db.add_all(cultivos)
    db.commit()
    
    # Asignar cultivos a cajones (ejemplo)
    asignaciones = [
        models.AsignacionCultivo(
            cajon_id=1,
            cultivo_id=1,  # Tomate
            fecha_inicio=date(2024, 5, 1),
            fecha_fin=date(2024, 9, 30),
            notas="Plantar en primavera"
        ),
        models.AsignacionCultivo(
            cajon_id=1,
            cultivo_id=5,  # Albahaca
            fecha_inicio=date(2024, 5, 15),
            fecha_fin=date(2024, 10, 15),
            notas="Compañera del tomate"
        ),
        models.AsignacionCultivo(
            cajon_id=2,
            cultivo_id=2,  # Lechuga
            fecha_inicio=date(2024, 4, 1),
            fecha_fin=date(2024, 7, 31),
            notas="Cosechar antes del calor extremo"
        ),
        models.AsignacionCultivo(
            cajon_id=3,
            cultivo_id=3,  # Zanahoria
            fecha_inicio=date(2024, 3, 15),
            fecha_fin=date(2024, 6, 30),
            notas="Suelo profundo"
        )
    ]
    db.add_all(asignaciones)
    db.commit()
    
    # Crear datos climáticos de ejemplo (opcional)
    clima = models.Clima(
        huerto_id=huerto.id,
        fecha=date(2024, 5, 20),
        temperatura_min=15.0,
        temperatura_max=28.0,
        humedad_relativa=60.0,
        precipitacion=0.0,
        velocidad_viento=10.0,
        direccion_viento="NE",
        radiacion_solar=500.0
    )
    db.add(clima)
    db.commit()
    
    print("Datos iniciales cargados correctamente.")
