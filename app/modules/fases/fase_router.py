from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import PaginatedData, PaginatedResponse, PaginationMeta, ResponseBase
from app.db.database import get_db
from app.modules.fases.fase_schema import (
    FaseCreateDTO,
    FasePreparacionCreateDTO,
    FasePreparacionResponseDTO,
    FasePruebaCreateDTO,
    FasePruebaResponseDTO,
    FaseResponseDTO,
    FaseUpdateDTO,
)
from app.modules.fases.fase_service import FaseService


router = APIRouter(prefix="/fases", tags=["fases"])


@router.get("", response_model=PaginatedResponse[FaseResponseDTO])
def listar_fases(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    service = FaseService(db)
    items, total = service.get_all(page=page, limit=limit)
    meta = PaginationMeta(page=page, limit=limit, total=total, total_pages=(total + limit - 1) // limit)
    data = PaginatedData(items=items, meta=meta)
    return PaginatedResponse(data=data, message="Lista obtenida correctamente")


@router.get("/{fase_id}", response_model=ResponseBase[FaseResponseDTO])
def obtener_fase(fase_id: int, db: Session = Depends(get_db)):
    service = FaseService(db)
    fase = service.get_by_id(fase_id)
    return ResponseBase(data=fase, message="Operacion exitosa")


@router.post("", response_model=ResponseBase[FaseResponseDTO])
def crear_fase(data: FaseCreateDTO, db: Session = Depends(get_db)):
    service = FaseService(db)
    fase = service.create(data)
    return ResponseBase(data=fase, message="Operacion exitosa")


@router.put("/{fase_id}", response_model=ResponseBase[FaseResponseDTO])
def actualizar_fase(fase_id: int, data: FaseUpdateDTO, db: Session = Depends(get_db)):
    service = FaseService(db)
    fase = service.update(fase_id, data)
    return ResponseBase(data=fase, message="Operacion exitosa")


@router.delete("/{fase_id}", response_model=ResponseBase[FaseResponseDTO])
def eliminar_fase(fase_id: int, db: Session = Depends(get_db)):
    service = FaseService(db)
    fase = service.get_by_id(fase_id)
    service.delete(fase_id)
    return ResponseBase(data=fase, message="Operacion exitosa")


@router.post("/prueba", response_model=ResponseBase[FasePruebaResponseDTO])
def crear_fase_prueba(data: FasePruebaCreateDTO, db: Session = Depends(get_db)):
    service = FaseService(db)
    resultado = service.create_fase_prueba(data)
    return ResponseBase(data=resultado, message="Operacion exitosa")


@router.post("/preparacion", response_model=ResponseBase[FasePreparacionResponseDTO])
def crear_fase_preparacion(data: FasePreparacionCreateDTO, db: Session = Depends(get_db)):
    service = FaseService(db)
    resultado = service.create_fase_preparacion(data)
    return ResponseBase(data=resultado, message="Operacion exitosa")
