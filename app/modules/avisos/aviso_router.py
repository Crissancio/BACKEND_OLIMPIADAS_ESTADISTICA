from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.core.responses import PaginatedData, PaginatedResponse, PaginationMeta, ResponseBase
from app.db.database import get_db
from app.modules.avisos.aviso_schema import AvisoCreateDTO, AvisoResponseDTO, AvisoUpdateDTO
from app.modules.avisos.aviso_service import AvisoService


router = APIRouter(prefix="/avisos", tags=["avisos"])


@router.get("", response_model=PaginatedResponse[AvisoResponseDTO])
def listar_avisos(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    service = AvisoService(db)
    items, total = service.get_public(page=page, limit=limit)
    meta = PaginationMeta(page=page, limit=limit, total=total, total_pages=(total + limit - 1) // limit)
    data = PaginatedData(items=items, meta=meta)
    return PaginatedResponse(data=data, message="Lista obtenida correctamente")


@router.get("/admin", response_model=PaginatedResponse[AvisoResponseDTO])
def listar_avisos_admin(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_admin_id: int = Depends(get_current_admin),
):
    service = AvisoService(db)
    items, total = service.get_all(page=page, limit=limit)
    meta = PaginationMeta(page=page, limit=limit, total=total, total_pages=(total + limit - 1) // limit)
    data = PaginatedData(items=items, meta=meta)
    return PaginatedResponse(data=data, message="Lista obtenida correctamente")


@router.get("/{aviso_id}", response_model=ResponseBase[AvisoResponseDTO])
def obtener_aviso(aviso_id: int, db: Session = Depends(get_db)):
    service = AvisoService(db)
    aviso = service.get_public_by_id(aviso_id)
    return ResponseBase(data=aviso, message="Operacion exitosa")


@router.post("", response_model=ResponseBase[AvisoResponseDTO])
def crear_aviso(
    data: AvisoCreateDTO,
    db: Session = Depends(get_db),
    current_admin_id: int = Depends(get_current_admin),
):
    service = AvisoService(db)
    aviso = service.create(data, current_admin_id)
    return ResponseBase(data=aviso, message="Operacion exitosa")


@router.put("/{aviso_id}", response_model=ResponseBase[AvisoResponseDTO])
def actualizar_aviso(
    aviso_id: int,
    data: AvisoUpdateDTO,
    db: Session = Depends(get_db),
    current_admin_id: int = Depends(get_current_admin),
):
    service = AvisoService(db)
    aviso = service.update(aviso_id, data, current_admin_id)
    return ResponseBase(data=aviso, message="Operacion exitosa")


@router.delete("/{aviso_id}", response_model=ResponseBase[AvisoResponseDTO])
def eliminar_aviso(
    aviso_id: int,
    db: Session = Depends(get_db),
    current_admin_id: int = Depends(get_current_admin),
):
    service = AvisoService(db)
    aviso = service.delete(aviso_id, current_admin_id)
    return ResponseBase(data=aviso, message="Operacion exitosa")
