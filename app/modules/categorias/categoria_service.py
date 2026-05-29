from sqlalchemy.orm import Session
from app.core.exceptions import BusinessRuleError, NotFoundError
from app.modules.categorias.categoria_model import CategoriaModel, EstadoEntidad
from app.modules.categorias.categoria_repository import CategoriaRepository
from app.modules.categorias.categoria_schema import CategoriaCreateDTO, CategoriaEstadoUpdateDTO, CategoriaUpdateDTO

class CategoriaService:
    def __init__(self, db: Session):
        self.repository = CategoriaRepository(db)

    def get_by_id(self, categoria_id: int):
        categoria = self.repository.get_by_id(categoria_id)
        if not categoria:
            raise NotFoundError("Categoría no encontrada")
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
                "estado": categoria.estado
            }
            for categoria in categorias
        ]

    def create(self, data: CategoriaCreateDTO):
        nueva_categoria = CategoriaModel(
            id_convocatoria=data.id_convocatoria,
            nombre_categoria=data.nombre_categoria,
            curso=data.curso,
            nivel=data.nivel,
            estado=EstadoEntidad.BORRADOR
        )
        return self.repository.create(nueva_categoria)

    def update(self, categoria_id: int, data: CategoriaUpdateDTO):
        categoria = self.get_by_id(categoria_id)
        updates = data.model_dump(exclude_unset=True)

        if not updates:
            return categoria

        if categoria.estado == EstadoEntidad.ELIMINADA:
            raise BusinessRuleError("No se puede editar una categoría ELIMINADA.")

        if categoria.estado == EstadoEntidad.LISTA:
            if "curso" in updates or "nivel" in updates:
                raise BusinessRuleError("Una categoría en estado LISTA solo permite editar el nombre.")

        for key, value in updates.items():
            setattr(categoria, key, value)

        return self.repository.update(categoria)

    def cambiar_estado(self, categoria_id: int, data: CategoriaEstadoUpdateDTO):
        categoria = self.get_by_id(categoria_id)
        estado_actual = categoria.estado
        nuevo_estado = data.estado

        if estado_actual == nuevo_estado:
            return categoria

        if nuevo_estado == EstadoEntidad.BORRADOR:
            raise BusinessRuleError("No se puede regresar al estado BORRADOR bajo ninguna circunstancia.")

        if estado_actual == EstadoEntidad.BORRADOR and nuevo_estado != EstadoEntidad.LISTA:
            raise BusinessRuleError("De BORRADOR solo se puede pasar a LISTA.")

        if estado_actual == EstadoEntidad.LISTA and nuevo_estado == EstadoEntidad.ELIMINADA:
            if hasattr(categoria, "inscripciones") and len(categoria.inscripciones) > 0:
                raise BusinessRuleError("No se puede eliminar (baja lógica) una categoría con inscripciones registradas.")

        if estado_actual == EstadoEntidad.ELIMINADA and nuevo_estado != EstadoEntidad.LISTA:
            raise BusinessRuleError("De ELIMINADA solo se puede restaurar a LISTA.")

        categoria.estado = nuevo_estado
        return self.repository.update(categoria)

    def delete(self, categoria_id: int):
        categoria = self.get_by_id(categoria_id)

        if categoria.estado not in [EstadoEntidad.BORRADOR, EstadoEntidad.ELIMINADA]:
            raise BusinessRuleError("Solo se puede realizar la eliminación física si la categoría está en BORRADOR o ELIMINADA.")

        if hasattr(categoria, "inscripciones") and len(categoria.inscripciones) > 0:
            raise BusinessRuleError("No se puede eliminar físicamente una categoría que tenga inscripciones registradas.")
        self.repository.delete(categoria)
        return categoria