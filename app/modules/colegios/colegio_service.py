from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.modules.colegios.colegio_model import ColegioModel
from app.modules.colegios.colegio_repository import ColegioRepository
from app.modules.colegios.colegio_schema import ColegioCreateDTO, ColegioUpdateDTO


class ColegioService:
    def __init__(self, db: Session):
        self.repository = ColegioRepository(db)

    def get_by_id(self, colegio_id: int):
        colegio = self.repository.get_by_id(colegio_id)
        if not colegio:
            raise NotFoundError("Colegio no encontrado")
        return colegio

    def get_all(self, page: int, limit: int):
        skip = (page - 1) * limit
        items = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count_all()
        return items, total

    def create(self, data: ColegioCreateDTO):
        colegio = ColegioModel(**data.model_dump())
        return self.repository.create(colegio)

    def update(self, colegio_id: int, data: ColegioUpdateDTO):
        colegio = self.get_by_id(colegio_id)
        updates = data.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(colegio, key, value)
        return self.repository.update(colegio)
