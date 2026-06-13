from sqlalchemy import Column, Integer, Numeric, Boolean, String, DateTime
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

    estado_alerta = Column(String)

    fecha_hora = Column(DateTime)