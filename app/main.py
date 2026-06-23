from fastapi import FastAPI
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal
from app.models import Medicion
from app.schemas import MedicionCreate

app = FastAPI()


@app.get("/")
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
    estado_alerta=datos.estado_alerta,
    fecha_hora=datetime.now()
)

    db.add(nueva_medicion)

    db.commit()

    db.close()

    return {
        "mensaje": "medicion guardada"
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