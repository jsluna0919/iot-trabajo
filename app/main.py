from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.database import SessionLocal
from app.models import Medicion, Alerta, configuracion_Alerta
from app.schemas import MedicionCreate, MedicionResponse, AlertaCreate, AlertaResponse, Configuracion_AlertaCreate, Configuracion_AlertaResponse, NotificacionCreate,NotificacionResponse, UsuarioCreate, UsuarioResponse
from typing import List

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

@app.get("/mediciones", response_model=List[MedicionResponse])
def obtener_mediciones():

    db: Session = SessionLocal()

    mediciones = db.query(Medicion).all()

    db.close()

    return mediciones

@app.post("/alerta")
def crear_alerta(datos: AlertaCreate):

    db: Session = SessionLocal()

    nueva_alerta = Alerta(
        nivel_alerta=datos.nivel_alerta,
        descripcion=datos.descripcion,
        atendida=datos.atendida
    )

    db.add(nueva_alerta)
    db.commit()

    db.close()

    return {
        "mensaje": "alerta guardada"
    }

@app.get("/alertas", response_model=List[AlertaResponse])
def obtener_alertas():

    db: Session = SessionLocal()

    alertas = db.query(Alerta).all()

    db.close()

    return alertas

@app.post("/configuracion-alertas")
def crear_configuracion(
        datos: Configuracion_AlertaCreate):

    db: Session = SessionLocal()

    configuracion = configuracion_Alerta(
        nivel_preventivo=datos.nivel_preventivo,
        nivel_critico=datos.nivel_critico,
        activo=datos.activo
    )

    db.add(configuracion)
    db.commit()

    db.close()

    return {
        "mensaje": "Configuración creada correctamente"
    }

from typing import List

@app.get(
    "/configuracion-alertas",
    response_model=List[Configuracion_AlertaResponse]
)
def obtener_configuraciones():

    db: Session = SessionLocal()

    configuraciones = (
        db.query(configuracion_Alerta)
        .all()
    )

    db.close()

    return configuraciones

from app.models import (
    Medicion,
    Alerta,
    ConfiguracionAlerta,
    Notificacion,
    Usuario
)

@app.post("/usuarios")
def crear_usuario(
        datos: UsuarioCreate):

    db: Session = SessionLocal()

    usuario = Usuario(
        nombre=datos.nombre,
        cedula=datos.cedula,
        correo=datos.correo,
        contrasena=datos.contrasena,
        rol=datos.rol
    )

    db.add(usuario)
    db.commit()

    db.close()

    return {
        "mensaje": "Usuario creado correctamente"
    }

from typing import List

@app.get(
    "/usuarios",
    response_model=List[UsuarioResponse]
)
def obtener_usuarios():

    db: Session = SessionLocal()

    usuarios = (
        db.query(Usuario)
        .all()
    )

    db.close()

    return usuarios