from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class AvisoCreateDTO(BaseModel):
    titulo: str
    descripcion: str
    tipo: str
    prioridad: str = "MEDIA"
    fecha_publicacion: Optional[datetime] = None

class AvisoUpdateDTO(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    prioridad: Optional[str] = None
    fecha_publicacion: Optional[datetime] = None

class AvisoEstadoUpdateDTO(BaseModel):
    estado: str

class AvisoResponseDTO(BaseModel):
    id_aviso: int
    titulo: str
    descripcion: str
    tipo: str
    prioridad: str
    fecha_creacion: datetime
    fecha_publicacion: Optional[datetime] = None
    estado: str
    estado_temporal: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)