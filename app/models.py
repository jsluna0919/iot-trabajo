from sqlalchemy import Column, Integer, Numeric, Boolean, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Medicion(Base):
    __tablename__ = "tbl_mediciones"

    id_medicion = Column(Integer, primary_key=True, index=True)

    nivel_agua = Column(Numeric)
    nivel_fluvial = Column(Numeric)

    temperatura = Column(Numeric)
    humedad = Column(Numeric)

    esta_lloviendo = Column(Boolean)

    estado_alerta = Column(String)

    fecha_hora = Column(DateTime, default=datetime.utcnow)

class Alerta(Base):
    __tablename__ = "tbl_alertas"

    id_alerta = Column(Integer, primary_key=True, index=True)

    nivel_alerta = Column(String)
    descripcion = Column(String)

    fecha_hora = Column(DateTime, default=datetime.utcnow)

    atendida = Column(Boolean)

class Configuracion_Alerta(Base):
    __tablename__="tbl_configuracion_alertas"

    id_configuracion=Column(Integer, primary_key=True, index=True)

    nivel_preventivo=Column(String)
    nivel_critico=Column(String)

    activo=Column(Boolean)

    fecha_actualizacion = Column(DateTime, default=datetime.utcnow)

class Notificacion(Base):
    __tablename__ = "tbl_notificaciones"

    id_notificaciones = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_alerta = Column(Integer)

    medio = Column(String)

    destinatario = Column(String)

    fecha_envio = Column(
        DateTime,
        default=datetime.utcnow
    )

    estado = Column(String)

from datetime import datetime

class Usuario(Base):
    __tablename__ = "tbl_usuarios"

    id_usuarios = Column(Integer, primary_key=True, index=True)

    nombre = Column(String)
    cedula = Column(String)
    correo = Column(String)
    contrasena = Column(String)
    rol = Column(String)

    fecha_registro = Column(
        DateTime,
        default=datetime.utcnow
    )
