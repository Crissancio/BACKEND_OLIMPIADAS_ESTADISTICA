from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ContactoCreateDTO(BaseModel):
    nombre_completo: str
    correo_electronico: str
    asunto: str
    mensaje: str


class ContactoUpdateDTO(BaseModel):
    estado: str


class ContactoResponseDTO(BaseModel):
    id_contacto: int
    nombre_completo: str
    correo_electronico: str
    asunto: str
    mensaje: str
    estado: str
    creado_en: datetime

    model_config = ConfigDict(from_attributes=True)
