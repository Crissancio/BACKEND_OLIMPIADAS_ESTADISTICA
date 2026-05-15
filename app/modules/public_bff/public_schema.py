from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from app.modules.avisos.aviso_schema import AvisoResponseDTO
from app.modules.convocatorias.convocatoria_schema import ConvocatoriaResponseDTO
from app.modules.materiales.material_schema import MaterialResponseDTO


class CategoriaResumenDTO(BaseModel):
    nombre_convocatoria: str
    nivel: str
    curso: int


class MaterialPrincipalDTO(BaseModel):
    enlace_acceso: Optional[str] = None
    mensaje: Optional[str] = None


class AvisoInicioDTO(BaseModel):
    titulo: str
    descripcion: str
    tipo: str
    fecha_publicacion: Optional[date] = None


class InicioResponseDTO(BaseModel):
    convocatoria: Optional[ConvocatoriaResponseDTO] = None
    material_principal: MaterialPrincipalDTO
    categorias: List[CategoriaResumenDTO]
    avisos: List[AvisoInicioDTO]


class ConvocatoriaDetalleDTO(BaseModel):
    convocatoria: Optional[ConvocatoriaResponseDTO] = None
    categorias: List[CategoriaResumenDTO]
    materiales: List[MaterialResponseDTO]
    afiche: Optional[MaterialResponseDTO] = None
    convocatoria_documento: Optional[MaterialResponseDTO] = None
    reglamento: Optional[MaterialResponseDTO] = None
