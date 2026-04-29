from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


class FaseBaseDTO(BaseModel):
    id_categoria_fk: int
    nombre_fase: str
    descripcion: Optional[str] = None
    modalidad: str
    estado: str


class FaseCreateDTO(FaseBaseDTO):
    pass


class FaseUpdateDTO(BaseModel):
    nombre_fase: Optional[str] = None
    descripcion: Optional[str] = None
    modalidad: Optional[str] = None
    estado: Optional[str] = None


class FaseResponseDTO(FaseBaseDTO):
    id_fase: int

    model_config = ConfigDict(from_attributes=True)


class FasePruebaCreateDTO(BaseModel):
    id_categoria_fk: int
    nombre_fase: str
    descripcion: Optional[str] = None
    modalidad: str
    estado: str
    id_fase_anterior: Optional[int] = None
    criterio_aprobacion: int
    fecha_realizacion: datetime
    lugar_realizacion: Optional[str] = None


class FasePruebaResponseDTO(BaseModel):
    id_fase: int
    id_categoria_fk: int
    nombre_fase: str
    descripcion: Optional[str] = None
    modalidad: str
    estado: str
    id_fase_anterior: Optional[int] = None
    criterio_aprobacion: int
    fecha_realizacion: datetime
    lugar_realizacion: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class FasePreparacionCreateDTO(BaseModel):
    id_categoria_fk: int
    nombre_fase: str
    descripcion: Optional[str] = None
    modalidad: str
    estado: str
    fecha_inicio: datetime
    fecha_fin: datetime


class FasePreparacionResponseDTO(BaseModel):
    id_fase: int
    id_categoria_fk: int
    nombre_fase: str
    descripcion: Optional[str] = None
    modalidad: str
    estado: str
    fecha_inicio: datetime
    fecha_fin: datetime

    model_config = ConfigDict(from_attributes=True)
