from typing import Optional
from pydantic import BaseModel, ConfigDict

class PublicColaboradorResponseDTO(BaseModel):
    nombres: str
    paterno: str
    materno: Optional[str]
    perfil: Optional[str]
    presentacion: Optional[str]
    rol: str
    correo: str

    model_config = ConfigDict(from_attributes=True)