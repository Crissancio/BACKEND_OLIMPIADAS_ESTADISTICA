from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.core.responses import PaginatedData, PaginatedResponse, PaginationMeta, ResponseBase
from app.db.database import get_db
from app.modules.personas.persona_schema import (
    ColaboradorCreateDTO,
    ColaboradorResponseDTO,
    DirectorCreateDTO,
    DirectorResponseDTO,
    EstudianteCreateDTO,
    EstudianteResponseDTO,
)
from app.modules.personas.persona_service import PersonaService


router = APIRouter(prefix="/personas", tags=["personas"])


@router.get("/estudiantes", response_model=PaginatedResponse[EstudianteResponseDTO])
def listar_estudiantes(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    service = PersonaService(db)
    items, total = service.list_estudiantes(page=page, limit=limit)
    meta = PaginationMeta(page=page, limit=limit, total=total, total_pages=(total + limit - 1) // limit)
    data = PaginatedData(items=items, meta=meta)
    return PaginatedResponse(data=data, message="Lista obtenida correctamente")


@router.get("/directores", response_model=PaginatedResponse[DirectorResponseDTO])
def listar_directores(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    service = PersonaService(db)
    items, total = service.list_directores(page=page, limit=limit)
    meta = PaginationMeta(page=page, limit=limit, total=total, total_pages=(total + limit - 1) // limit)
    data = PaginatedData(items=items, meta=meta)
    return PaginatedResponse(data=data, message="Lista obtenida correctamente")


@router.get("/colaboradores", response_model=PaginatedResponse[ColaboradorResponseDTO])
def listar_colaboradores(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    service = PersonaService(db)
    items, total = service.list_colaboradores(page=page, limit=limit)
    meta = PaginationMeta(page=page, limit=limit, total=total, total_pages=(total + limit - 1) // limit)
    data = PaginatedData(items=items, meta=meta)
    return PaginatedResponse(data=data, message="Lista obtenida correctamente")


@router.post("/estudiantes", response_model=ResponseBase[EstudianteResponseDTO])
def crear_estudiante(
    data: EstudianteCreateDTO,
    db: Session = Depends(get_db),
    current_admin_id: int = Depends(get_current_admin),
):
    service = PersonaService(db)
    estudiante = service.create_estudiante(data)
    return ResponseBase(data=estudiante, message="Operacion exitosa")


@router.post("/directores", response_model=ResponseBase[DirectorResponseDTO])
def crear_director(
    data: DirectorCreateDTO,
    db: Session = Depends(get_db),
    current_admin_id: int = Depends(get_current_admin),
):
    service = PersonaService(db)
    director = service.create_director(data)
    return ResponseBase(data=director, message="Operacion exitosa")


@router.post("/colaboradores", response_model=ResponseBase[ColaboradorResponseDTO])
def crear_colaborador(
    data: ColaboradorCreateDTO,
    db: Session = Depends(get_db),
    current_admin_id: int = Depends(get_current_admin),
):
    service = PersonaService(db)
    colaborador = service.create_colaborador(data)
    return ResponseBase(data=colaborador, message="Operacion exitosa")
