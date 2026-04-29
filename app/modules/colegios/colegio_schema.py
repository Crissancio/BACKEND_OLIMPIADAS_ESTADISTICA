from typing import Optional

from pydantic import BaseModel, ConfigDict


class ColegioBaseDTO(BaseModel):
    codigo: int
    nombre: str
    tipo: str
    turno: str
    departamento: str
    municipio: str
    calle: Optional[str] = None
    numero: Optional[str] = None
    estado: str


class ColegioCreateDTO(ColegioBaseDTO):
    pass


class ColegioUpdateDTO(BaseModel):
    codigo: Optional[int] = None
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    turno: Optional[str] = None
    departamento: Optional[str] = None
    municipio: Optional[str] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    estado: Optional[str] = None


class ColegioResponseDTO(ColegioBaseDTO):
    id_colegio: int

    model_config = ConfigDict(from_attributes=True)
