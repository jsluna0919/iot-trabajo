from pydantic import BaseModel


class MedicionCreate(BaseModel):

    id_dispositivo: str
    nivel_agua: float
    nivel_fluvial: float
    temperatura: float
    humedad: float
    esta_lloviendo: bool
    estado_alerta: int


class ConfiguracionUpdate(BaseModel):
    nivel_preventivo: float
    nivel_critico: float
    activo: bool