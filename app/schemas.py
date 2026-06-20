from pydantic import BaseModel
from datetime import datetime

class MedicionCreate(BaseModel):
    nivel_agua: float
    nivel_fluvial: float
    temperatura: float
    humedad: float
    esta_lloviendo: bool
    estado_alerta: str


class MedicionResponse(BaseModel):
    id_medicion: int
    nivel_agua: float
    nivel_fluvial: float
    temperatura: float
    humedad: float
    esta_lloviendo: bool
    estado_alerta: str
    fecha_hora: datetime | None

    class Config:
        from_attributes = True

class AlertaCreate(BaseModel):
    nivel_alerta: str
    descripcion: str
    atendida: bool


class AlertaResponse(BaseModel):
    id_alerta: int
    nivel_alerta: str
    descripcion: str
    fecha_hora: datetime | None
    atendida: bool

    class Config:
        from_attributes = True

class AlertaCreate(BaseModel):
    nivel_alerta: str
    descripcion: str
    atendida: bool


class Configuracion_AlertaCreate(BaseModel):
    
    nivel_preventivo: str
    nivel_critico: str
    activo: bool
   

class Configuracion_AlertaResponse(BaseModel):
    
    id_configuracion:int
    nivel_preventivo: str
    nivel_critico: str
    activo: bool
    fecha_actualizacion: datetime | None

    class Config:
        from_attributes = True

class NotificacionCreate(BaseModel):
    id_alerta: int
    medio: str
    destinatario: str
    estado: str

class NotificacionResponse(BaseModel):
    id_notificaciones: int
    id_alerta: int
    medio: str
    destinatario: str
    fecha_envio: datetime | None
    estado: str

    class Config:
        from_attributes = True

class UsuarioCreate(BaseModel):
    nombre: str
    cedula: str
    correo: str
    contrasena: str
    rol: str

class UsuarioResponse(BaseModel):
    id_usuarios: int
    nombre: str
    cedula: str
    correo: str
    rol: str
    fecha_registro: datetime | None

    class Config:
        from_attributes = True