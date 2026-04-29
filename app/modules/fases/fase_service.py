from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.modules.fases.fase_model import FaseModel, FasePreparacionModel, FasePruebaModel
from app.modules.fases.fase_repository import FaseRepository
from app.modules.fases.fase_schema import (
    FaseCreateDTO,
    FasePreparacionCreateDTO,
    FasePruebaCreateDTO,
    FaseUpdateDTO,
)


class FaseService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = FaseRepository(db)

    def get_by_id(self, fase_id: int):
        fase = self.repository.get_by_id(fase_id)
        if not fase:
            raise NotFoundError("Fase no encontrada")
        return fase

    def get_all(self, page: int, limit: int):
        skip = (page - 1) * limit
        items = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count_all()
        return items, total

    def create(self, fase_data: FaseCreateDTO):
        fase = FaseModel(**fase_data.model_dump())
        return self.repository.create(fase)

    def update(self, fase_id: int, data: FaseUpdateDTO):
        fase = self.get_by_id(fase_id)
        updates = data.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(fase, key, value)
        return self.repository.update(fase)

    def delete(self, fase_id: int):
        fase = self.get_by_id(fase_id)
        self.repository.delete(fase)

    def create_fase_prueba(self, data: FasePruebaCreateDTO):
        with self.db.begin():
            fase = FaseModel(
                id_categoria_fk=data.id_categoria_fk,
                nombre_fase=data.nombre_fase,
                descripcion=data.descripcion,
                modalidad=data.modalidad,
                estado=data.estado,
            )
            self.db.add(fase)
            self.db.flush()
            fase_prueba = FasePruebaModel(
                id_fase=fase.id_fase,
                id_fase_anterior=data.id_fase_anterior,
                criterio_aprobacion=data.criterio_aprobacion,
                fecha_realizacion=data.fecha_realizacion,
                lugar_realizacion=data.lugar_realizacion,
            )
            self.db.add(fase_prueba)

        self.db.refresh(fase)
        self.db.refresh(fase_prueba)
        return {
            "id_fase": fase.id_fase,
            "id_categoria_fk": fase.id_categoria_fk,
            "nombre_fase": fase.nombre_fase,
            "descripcion": fase.descripcion,
            "modalidad": fase.modalidad,
            "estado": fase.estado,
            "id_fase_anterior": fase_prueba.id_fase_anterior,
            "criterio_aprobacion": fase_prueba.criterio_aprobacion,
            "fecha_realizacion": fase_prueba.fecha_realizacion,
            "lugar_realizacion": fase_prueba.lugar_realizacion,
        }

    def create_fase_preparacion(self, data: FasePreparacionCreateDTO):
        with self.db.begin():
            fase = FaseModel(
                id_categoria_fk=data.id_categoria_fk,
                nombre_fase=data.nombre_fase,
                descripcion=data.descripcion,
                modalidad=data.modalidad,
                estado=data.estado,
            )
            self.db.add(fase)
            self.db.flush()
            fase_preparacion = FasePreparacionModel(
                id_fase=fase.id_fase,
                fecha_inicio=data.fecha_inicio,
                fecha_fin=data.fecha_fin,
            )
            self.db.add(fase_preparacion)

        self.db.refresh(fase)
        self.db.refresh(fase_preparacion)
        return {
            "id_fase": fase.id_fase,
            "id_categoria_fk": fase.id_categoria_fk,
            "nombre_fase": fase.nombre_fase,
            "descripcion": fase.descripcion,
            "modalidad": fase.modalidad,
            "estado": fase.estado,
            "fecha_inicio": fase_preparacion.fecha_inicio,
            "fecha_fin": fase_preparacion.fecha_fin,
        }

    def validate_dependencia(self, fase_id: int, fase_anterior_id: int):
        if fase_id == fase_anterior_id:
            raise BusinessRuleError("La fase anterior no puede ser la misma fase")
