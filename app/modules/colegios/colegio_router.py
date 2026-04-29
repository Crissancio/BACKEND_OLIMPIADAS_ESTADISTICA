from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import PaginatedData, PaginatedResponse, PaginationMeta, ResponseBase
from app.db.database import get_db
from app.modules.colegios.colegio_schema import ColegioCreateDTO, ColegioResponseDTO, ColegioUpdateDTO
from app.modules.colegios.colegio_service import ColegioService


router = APIRouter(prefix="/colegios", tags=["colegios"])


@router.get("", response_model=PaginatedResponse[ColegioResponseDTO])
def listar_colegios(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    service = ColegioService(db)
    items, total = service.get_all(page=page, limit=limit)
    meta = PaginationMeta(page=page, limit=limit, total=total, total_pages=(total + limit - 1) // limit)
    data = PaginatedData(items=items, meta=meta)
    return PaginatedResponse(data=data, message="Lista obtenida correctamente")


@router.get("/{colegio_id}", response_model=ResponseBase[ColegioResponseDTO])
def obtener_colegio(colegio_id: int, db: Session = Depends(get_db)):
    service = ColegioService(db)
    colegio = service.get_by_id(colegio_id)
    return ResponseBase(data=colegio, message="Operacion exitosa")


@router.post("", response_model=ResponseBase[ColegioResponseDTO])
def crear_colegio(data: ColegioCreateDTO, db: Session = Depends(get_db)):
    service = ColegioService(db)
    colegio = service.create(data)
    return ResponseBase(data=colegio, message="Operacion exitosa")


@router.put("/{colegio_id}", response_model=ResponseBase[ColegioResponseDTO])
def actualizar_colegio(colegio_id: int, data: ColegioUpdateDTO, db: Session = Depends(get_db)):
    service = ColegioService(db)
    colegio = service.update(colegio_id, data)
    return ResponseBase(data=colegio, message="Operacion exitosa")
