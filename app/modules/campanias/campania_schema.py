from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.modules.campanias.campania_model import EstadoCampania

class EnlaceDTO(BaseModel):
    url: str
    texto: str

class ColegioMinimoDTO(BaseModel):
    nombre: str
    model_config = ConfigDict(from_attributes=True)

class EstudianteDestinatarioDTO(BaseModel):
    id_estudiante: int
    nombres: str
    paterno: str
    materno: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[int] = None
    colegio: Optional[ColegioMinimoDTO] = None
    
    model_config = ConfigDict(from_attributes=True)

class CampaniaDestinatarioDTO(BaseModel):
    estudiante: EstudianteDestinatarioDTO
    model_config = ConfigDict(from_attributes=True)

class CampaniaCreateDTO(BaseModel):
    nombre: str
    asunto: str
    contenido_mensaje: str
    contenido_secundario: Optional[str] = None
    enlaces: Optional[List[EnlaceDTO]] = []
    fecha_programada: Optional[datetime] = None
    destinatarios_ids: Optional[List[int]] = []

class CampaniaUpdateDTO(BaseModel):
    nombre: Optional[str] = None
    asunto: Optional[str] = None
    contenido_mensaje: Optional[str] = None
    contenido_secundario: Optional[str] = None
    enlaces: Optional[List[EnlaceDTO]] = None
    fecha_programada: Optional[datetime] = None
    agregar_destinatarios: Optional[List[int]] = []
    eliminar_destinatarios: Optional[List[int]] = []

class EstadoUpdateDTO(BaseModel):
    estado: EstadoCampania

class CampaniaResponseDTO(BaseModel):
    id: int
    nombre: str
    asunto: str
    contenido_mensaje: str
    contenido_secundario: Optional[str] = None
    enlaces: Optional[List[EnlaceDTO]] = []
    estado: EstadoCampania
    fecha_creacion: datetime
    fecha_programada: Optional[datetime]
    destinatarios: List[CampaniaDestinatarioDTO] = []
    
    model_config = ConfigDict(from_attributes=True)