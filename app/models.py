from sqlalchemy import Column, Integer, Float, Boolean, String, DateTime,Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Medicion(Base):
    __tablename__ = "tbl_mediciones"
    id_medicion = Column(Integer, primary_key=True, index=True)
    nivel_agua = Column(Numeric)
    nivel_fluvial = Column(Numeric)
    temperatura = Column(Numeric)
    humedad = Column(Numeric)
    esta_lloviendo = Column(Boolean)
    estado_alerta = Column(Integer, nullable=False)
    fecha_hora = Column(DateTime)
    id_dispositivo = Column(String(20),nullable=False, default="esp1")

class Alerta(Base):
    __tablename__ = "tbl_alertas"
    id_alerta = Column(Integer, primary_key=True, index=True)
    nivel_alerta = Column(String)
    descripcion = Column(String)
    fecha_hora = Column(DateTime)
    atendida = Column(Boolean)


class ConfiguracionAlerta(Base):
    __tablename__ = "tbl_configuracion_alertas"

    id_configuracion = Column(Integer, primary_key=True, index=True)
    nivel_preventivo = Column(Float)
    nivel_critico = Column(Float)
    activo = Column(Boolean)
    fecha_actualizacion = Column(DateTime)