from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from app.database import SessionLocal
from app.models import Medicion, Alerta, ConfiguracionAlerta
from app.schemas import MedicionCreate, ConfiguracionUpdate

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],      # Permite todos los métodos HTTP
    allow_headers=["*"],      # Permite todos los encabezados
)

# coordenadas 
LATITUD_SENSOR = 6.407003
LONGITUD_SENSOR = -75.446880

@app.post("/mediciones")
def crear_medicion(datos: MedicionCreate):

    db: Session = SessionLocal()

    nueva_medicion = Medicion(
        id_dispositivo=datos.id_dispositivo,
        nivel_agua=datos.nivel_agua,
        nivel_fluvial=datos.nivel_fluvial,
        temperatura=datos.temperatura,
        humedad=datos.humedad,
        esta_lloviendo=datos.esta_lloviendo,
        estado_alerta=datos.estado_alerta,
        fecha_hora=datetime.now()
    )

    db.add(nueva_medicion)
    db.commit()
    db.refresh(nueva_medicion)

    # Crear alerta únicamente si el estado es diferente de verde
    if datos.estado_alerta > 1:

        niveles = {
            2: "AMARILLA",
            3: "NARANJA",
            4: "ROJA"
        }

        descripciones = {
            2: f"Nivel de agua en precaución: {datos.nivel_agua} cm",
            3: f"Nivel de agua en prevención: {datos.nivel_agua} cm",
            4: f"Nivel crítico detectado: {datos.nivel_agua} cm"
        }

        alerta = Alerta(
            nivel_alerta=niveles.get(datos.estado_alerta),
            descripcion=descripciones.get(datos.estado_alerta),
            fecha_hora=datetime.now(),
            atendida=False
        )

        db.add(alerta)
        db.commit()

    db.close()

    return {
        "mensaje": "Medición guardada correctamente",
        "id_medicion": nueva_medicion.id_medicion,
        "estado_alerta": nueva_medicion.estado_alerta
    }


@app.get("/mediciones")
def obtener_mediciones(
    fecha: date = None,
    hora: int = None
):

    db: Session = SessionLocal()

    consulta = db.query(Medicion)

    # Filtrar por fecha
    if fecha:
        consulta = consulta.filter(
            func.date(Medicion.fecha_hora) == fecha
        )

    # Filtrar por hora
    if hora is not None:
        consulta = consulta.filter(
            func.extract('hour', Medicion.fecha_hora) == hora
        )

    mediciones = consulta.order_by(
        Medicion.id_medicion.desc()
    ).all()

    resultado = []

    for m in mediciones:
        resultado.append({
            "id_medicion": m.id_medicion,
            "id_dispositivo": m.id_dispositivo,
            "nivel_agua": float(m.nivel_agua),
            "nivel_fluvial": float(m.nivel_fluvial),
            "temperatura": float(m.temperatura),
            "humedad": float(m.humedad),
            "esta_lloviendo": m.esta_lloviendo,
            "estado_alerta": m.estado_alerta,
            "fecha_hora": str(m.fecha_hora)
        })

    db.close()

    return resultado


@app.get("/mediciones/ultima")
def obtener_ultima_medicion():

    db: Session = SessionLocal()

    medicion = (
        db.query(Medicion)
        .order_by(Medicion.id_medicion.desc())
        .first()
    )

    db.close()

    if not medicion:
        return {"mensaje": "No hay mediciones"}

    return {
        "id_medicion": medicion.id_medicion,
        "nivel_agua": float(medicion.nivel_agua),
        "nivel_fluvial": float(medicion.nivel_fluvial),
        "temperatura": float(medicion.temperatura),
        "humedad": float(medicion.humedad),
        "esta_lloviendo": medicion.esta_lloviendo,
        "estado_alerta": medicion.estado_alerta,
        "fecha_hora": str(medicion.fecha_hora)
    }


@app.get("/alertas")
def obtener_alertas():

    db: Session = SessionLocal()

    alertas = (
        db.query(Alerta)
        .order_by(Alerta.id_alerta.desc())
        .all()
    )

    resultado = []

    for a in alertas:
        resultado.append({
            "id_alerta": a.id_alerta,
            "nivel_alerta": a.nivel_alerta,
            "descripcion": a.descripcion,
            "fecha_hora": str(a.fecha_hora),
            "atendida": a.atendida
        })

    db.close()

    return resultado


@app.get("/alertas/{id_alerta}")
def obtener_alerta(id_alerta: int):

    db: Session = SessionLocal()

    alerta = (
        db.query(Alerta)
        .filter(Alerta.id_alerta == id_alerta)
        .first()
    )

    db.close()

    if not alerta:
        return {"mensaje": "Alerta no encontrada"}

    return {
        "id_alerta": alerta.id_alerta,
        "nivel_alerta": alerta.nivel_alerta,
        "descripcion": alerta.descripcion,
        "fecha_hora": str(alerta.fecha_hora),
        "atendida": alerta.atendida
    }


@app.get("/configuracion-alertas")
def obtener_configuracion():

    db: Session = SessionLocal()

    config = (
        db.query(ConfiguracionAlerta)
        .filter(ConfiguracionAlerta.activo == True)
        .first()
    )

    db.close()

    if not config:
        return {"mensaje": "No existe configuración"}

    return {
        "id_configuracion": config.id_configuracion,
        "nivel_preventivo": float(config.nivel_preventivo),
        "nivel_critico": float(config.nivel_critico),
        "activo": config.activo,
        "fecha_actualizacion": str(config.fecha_actualizacion)
    }


@app.put("/configuracion-alertas")
def actualizar_configuracion(datos: ConfiguracionUpdate):

    db: Session = SessionLocal()

    config = (
        db.query(ConfiguracionAlerta)
        .first()
    )

    if not config:

        config = ConfiguracionAlerta(
            nivel_preventivo=datos.nivel_preventivo,
            nivel_critico=datos.nivel_critico,
            activo=datos.activo,
            fecha_actualizacion=datetime.now()
        )

        db.add(config)

    else:

        config.nivel_preventivo = datos.nivel_preventivo
        config.nivel_critico = datos.nivel_critico
        config.activo = datos.activo
        config.fecha_actualizacion = datetime.now()

    db.commit()
    db.close()

    return {
        "mensaje": "Configuración actualizada"
    }

@app.get("/mapa")
def obtener_datos_mapa():

    db: Session = SessionLocal()

    mediciones = (
        db.query(Medicion)
        .order_by(Medicion.id_medicion.desc())
        .all()
    )

    features = []

    for m in mediciones:

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    LONGITUD_SENSOR,
                    LATITUD_SENSOR
                ]
            },
            "properties": {
                "id_medicion": m.id_medicion,
                "nivel_agua": float(m.nivel_agua),
                "nivel_fluvial": float(m.nivel_fluvial),
                "temperatura": float(m.temperatura),
                "humedad": float(m.humedad),
                "esta_lloviendo": m.esta_lloviendo,
                "estado_alerta": m.estado_alerta,
                "fecha_hora": str(m.fecha_hora)
            }
        })

    db.close()

    return {
        "type": "FeatureCollection",
        "features": features
    }