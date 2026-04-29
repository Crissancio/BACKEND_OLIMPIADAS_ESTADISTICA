from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import PaginatedData, PaginatedResponse, PaginationMeta, ResponseBase
from app.db.database import get_db
from app.modules.categorias.categoria_schema import CategoriaCreateDTO, CategoriaResponseDTO, CategoriaUpdateDTO
from app.modules.categorias.categoria_service import CategoriaService


router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("", response_model=PaginatedResponse[CategoriaResponseDTO])
def listar_categorias(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    items, total = service.get_all(page=page, limit=limit)
    meta = PaginationMeta(page=page, limit=limit, total=total, total_pages=(total + limit - 1) // limit)
    data = PaginatedData(items=items, meta=meta)
    return PaginatedResponse(data=data, message="Lista obtenida correctamente")


@router.get("/{categoria_id}", response_model=ResponseBase[CategoriaResponseDTO])
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    categoria = service.get_by_id(categoria_id)
    return ResponseBase(data=categoria, message="Operacion exitosa")


@router.post("", response_model=ResponseBase[CategoriaResponseDTO])
def crear_categoria(data: CategoriaCreateDTO, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    categoria = service.create(data)
    return ResponseBase(data=categoria, message="Operacion exitosa")


@router.put("/{categoria_id}", response_model=ResponseBase[CategoriaResponseDTO])
def actualizar_categoria(categoria_id: int, data: CategoriaUpdateDTO, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    categoria = service.update(categoria_id, data)
    return ResponseBase(data=categoria, message="Operacion exitosa")


@router.delete("/{categoria_id}", response_model=ResponseBase[CategoriaResponseDTO])
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    categoria = service.delete(categoria_id)
    return ResponseBase(data=categoria, message="Operacion exitosa")
