from sqlalchemy.orm import Session

from app.modules.categorias.categoria_model import CategoriaModel


class CategoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, categoria_id: int):
        return (
            self.db.query(CategoriaModel)
            .filter(CategoriaModel.id_categoria == categoria_id)
            .first()
        )

    def get_all(self, skip: int, limit: int):
        return self.db.query(CategoriaModel).offset(skip).limit(limit).all()

    def count_all(self):
        return self.db.query(CategoriaModel).count()

    def get_by_convocatoria(self, convocatoria_id: int, skip: int, limit: int):
        return (
            self.db.query(CategoriaModel)
            .filter(CategoriaModel.id_convocatoria == convocatoria_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_by_convocatoria(self, convocatoria_id: int):
        return (
            self.db.query(CategoriaModel)
            .filter(CategoriaModel.id_convocatoria == convocatoria_id)
            .count()
        )

    def create(self, categoria: CategoriaModel):
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def update(self, categoria: CategoriaModel):
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def delete(self, categoria: CategoriaModel):
        self.db.delete(categoria)
        self.db.commit()
