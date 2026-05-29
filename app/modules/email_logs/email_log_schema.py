from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.modules.email_logs.email_log_model import EstadoEmail, TipoEmail

class EstudianteLogDTO(BaseModel):
    id_estudiante: int
    nombres: str
    paterno: str
    materno: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class EmailLogResponseDTO(BaseModel):
    id: int
    destinatario: str
    asunto: str
    tipo: TipoEmail
    estado: EstadoEmail
    error: Optional[str]
    intentos: int
    ultimo_intento: Optional[datetime]
    fecha_creacion: datetime
    fecha_envio: Optional[datetime]
    id_estudiante: Optional[int]
    id_contacto: Optional[int]
    id_campania: Optional[int]
    estudiante: Optional[EstudianteLogDTO] = None

    model_config = ConfigDict(from_attributes=True)