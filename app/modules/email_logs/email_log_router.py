from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.db.database import get_db
from app.modules.email_logs.email_log_schema import EmailLogResponseDTO
from app.modules.email_logs.email_log_service import EmailLogService
from app.core.responses import ResponseBase, PaginatedResponse, PaginationMeta

router = APIRouter(prefix="/email-logs", tags=["Email Logs"])

@router.get("/", response_model=PaginatedResponse[EmailLogResponseDTO])
def listar_logs(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    tipo: Optional[str] = None,
    estado: Optional[str] = None,
    id_campania: Optional[int] = None,
    es_estudiante: Optional[bool] = None,
    es_contacto: Optional[bool] = None,
    es_campania: Optional[bool] = None,
    busqueda: Optional[str] = None,
    creacion_start: Optional[datetime] = None,
    creacion_end: Optional[datetime] = None,
    envio_start: Optional[datetime] = None,
    envio_end: Optional[datetime] = None,
    intento_start: Optional[datetime] = None,
    intento_end: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    service = EmailLogService(db)
    items, total = service.listar_logs(
        page, limit, tipo=tipo, estado=estado, id_campania=id_campania,
        es_estudiante=es_estudiante, es_contacto=es_contacto, es_campania=es_campania,
        busqueda=busqueda, creacion_start=creacion_start, creacion_end=creacion_end,
        envio_start=envio_start, envio_end=envio_end,
        intento_start=intento_start, intento_end=intento_end
    )
    total_pages = (total + limit - 1) // limit
    return PaginatedResponse(
        success=True, message="Logs listados",
        data={"items": items, "meta": PaginationMeta(page=page, limit=limit, total=total, total_pages=total_pages)}
    )

@router.get("/{id}", response_model=ResponseBase[EmailLogResponseDTO])
def obtener_log(id: int, db: Session = Depends(get_db)):
    service = EmailLogService(db)
    return ResponseBase(success=True, message="Log encontrado", data=service.obtener_por_id(id))

@router.post("/reintentar-fallidos")
def reintentar_fallidos(db: Session = Depends(get_db)):
    service = EmailLogService(db)
    afectados = service.reintentar_fallidos()
    return ResponseBase(success=True, message=f"{afectados} correos pasados a PENDIENTE", data=None)