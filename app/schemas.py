from pydantic import BaseModel


class MedicionCreate(BaseModel):

    nivel_agua: float
    nivel_fluvial: float

    temperatura: float
    humedad: float

    esta_lloviendo: bool

    estado_alerta: str