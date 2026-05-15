from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.modules.categorias.categoria_model import CategoriaModel
from app.modules.categorias.categoria_repository import CategoriaRepository
from app.modules.categorias.categoria_schema import CategoriaCreateDTO, CategoriaUpdateDTO


class CategoriaService:
    def __init__(self, db: Session):
        self.repository = CategoriaRepository(db)

    def get_by_id(self, categoria_id: int):
        categoria = self.repository.get_by_id(categoria_id)
        if not categoria:
            raise NotFoundError("Categoria no encontrada")
        return categoria

    def get_all(self, page: int, limit: int):
        skip = (page - 1) * limit
        items = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count_all()
        return items, total

    def get_by_convocatoria(self, convocatoria_id: int, page: int, limit: int):
        skip = (page - 1) * limit
        items = self.repository.get_by_convocatoria(convocatoria_id, skip=skip, limit=limit)
        total = self.repository.count_by_convocatoria(convocatoria_id)
        return items, total

    def get_resumen_by_convocatoria(self, convocatoria_id: int):
        categorias = self.repository.get_resumen_by_convocatoria(convocatoria_id)
        return [
            {
                "id_categoria": categoria.id_categoria,
                "nombre_categoria": categoria.nombre_categoria,
                "nivel": categoria.nivel,
                "curso": categoria.curso,
            }
            for categoria in categorias
        ]

    def create(self, data: CategoriaCreateDTO):
        categoria = CategoriaModel(**data.model_dump())
        return self.repository.create(categoria)

    def update(self, categoria_id: int, data: CategoriaUpdateDTO):
        categoria = self.get_by_id(categoria_id)
        updates = data.model_dump(exclude_unset=True)
        if "curso" in updates or "nivel" in updates:
            raise BusinessRuleError("No se puede modificar curso o nivel con inscripciones asociadas")

        for key, value in updates.items():
            setattr(categoria, key, value)

        return self.repository.update(categoria)

    def delete(self, categoria_id: int):
        categoria = self.get_by_id(categoria_id)
        categoria.estado = "ELIMINADA"
        return self.repository.update(categoria)
