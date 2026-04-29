from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


class CategoriaBaseDTO(BaseModel):
    id_convocatoria: int
    nombre_categoria: str
    curso: int
    nivel: str
    estado: str


class CategoriaCreateDTO(CategoriaBaseDTO):
    pass


class CategoriaUpdateDTO(BaseModel):
    nombre_categoria: Optional[str] = None
    curso: Optional[int] = None
    nivel: Optional[str] = None
    estado: Optional[str] = None


class CategoriaResponseDTO(CategoriaBaseDTO):
    id_categoria: int

    model_config = ConfigDict(from_attributes=True)
