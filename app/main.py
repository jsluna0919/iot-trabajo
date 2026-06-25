from fastapi import FastAPI
from sqlalchemy.orm import Session
from datetime import datetime


from app.database import SessionLocal
from app.models import Medicion,Alerta,ConfiguracionAlerta
from app.schemas import MedicionCreate,ConfiguracionUpdate


app = FastAPI()


@app.get("/prueba")
def inicio():
    return {
        "mensaje": "API funcionando"
    }


@app.post("/mediciones")
def crear_medicion(datos: MedicionCreate):

    db: Session = SessionLocal()

    nueva_medicion = Medicion(
        nivel_agua=datos.nivel_agua,
        nivel_fluvial=datos.nivel_fluvial,
        temperatura=datos.temperatura,
        humedad=datos.humedad,
        esta_lloviendo=datos.esta_lloviendo,
        estado_alerta="SIN RIESGO",
        fecha_hora=datetime.now()
    )

    config = (
        db.query(ConfiguracionAlerta)
        .filter(ConfiguracionAlerta.activo == True)
        .first()
    )

    if config:

        # Nivel verde
        if 5 <= datos.nivel_agua < 10:

            nueva_medicion.estado_alerta = "NORMAL"

        # Alerta amarilla
        elif 10 <= datos.nivel_agua < 15:

            nueva_medicion.estado_alerta = "PRECAUCION"

            alerta = Alerta(
                nivel_alerta="AMARILLA",
                descripcion=f"Nivel de agua en precaución: {datos.nivel_agua} cm",
                fecha_hora=datetime.now(),
                atendida=False
            )

            db.add(alerta)

        # Alerta naranja
        elif 15 <= datos.nivel_agua <= 20:

            nueva_medicion.estado_alerta = "PREVENCION"

            alerta = Alerta(
                nivel_alerta="NARANJA",
                descripcion=f"Nivel de agua en prevención: {datos.nivel_agua} cm",
                fecha_hora=datetime.now(),
                atendida=False
            )

            db.add(alerta)

        # Alerta roja
        elif datos.nivel_agua > 20:

            nueva_medicion.estado_alerta = "CRITICA"

            alerta = Alerta(
                nivel_alerta="ROJA",
                descripcion=f"Nivel crítico detectado: {datos.nivel_agua} cm",
                fecha_hora=datetime.now(),
                atendida=False
            )

            db.add(alerta)

        else:

            nueva_medicion.estado_alerta = "SIN RIESGO"

    db.add(nueva_medicion)

    db.commit()

    db.refresh(nueva_medicion)

    db.close()

    return {
        "mensaje": "Medición guardada correctamente",
        "id_medicion": nueva_medicion.id_medicion,
        "estado_alerta": nueva_medicion.estado_alerta
    }

@app.get("/mediciones")
def obtener_mediciones():

    db: Session = SessionLocal()

    mediciones = db.query(Medicion)\
                   .order_by(Medicion.id_medicion.desc())\
                   .all()

    resultado = []

    for m in mediciones:
        resultado.append({
            "id_medicion": m.id_medicion,
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

    medicion = db.query(Medicion)\
                 .order_by(Medicion.id_medicion.desc())\
                 .first()

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
