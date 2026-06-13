from fastapi import FastAPI
from sqlalchemy.orm import Session

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
        estado_alerta=datos.estado_alerta
    )

    db.add(nueva_medicion)

    db.commit()

    db.close()

    return {
        "mensaje": "medicion guardada"
    }