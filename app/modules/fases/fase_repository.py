from sqlalchemy.orm import Session

from app.modules.fases.fase_model import FaseModel, FasePreparacionModel, FasePruebaModel


class FaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, fase_id: int):
        return self.db.query(FaseModel).filter(FaseModel.id_fase == fase_id).first()

    def get_all(self, skip: int, limit: int):
        return self.db.query(FaseModel).offset(skip).limit(limit).all()

    def count_all(self):
        return self.db.query(FaseModel).count()

    def get_by_categoria(self, categoria_id: int, skip: int, limit: int):
        return (
            self.db.query(FaseModel)
            .filter(FaseModel.id_categoria_fk == categoria_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_by_categoria(self, categoria_id: int):
        return self.db.query(FaseModel).filter(FaseModel.id_categoria_fk == categoria_id).count()

    def create(self, fase: FaseModel):
        self.db.add(fase)
        self.db.commit()
        self.db.refresh(fase)
        return fase

    def update(self, fase: FaseModel):
        self.db.commit()
        self.db.refresh(fase)
        return fase

    def delete(self, fase: FaseModel):
        self.db.delete(fase)
        self.db.commit()

    def create_fase_prueba(self, fase_prueba: FasePruebaModel):
        self.db.add(fase_prueba)
        self.db.commit()
        self.db.refresh(fase_prueba)
        return fase_prueba

    def create_fase_preparacion(self, fase_preparacion: FasePreparacionModel):
        self.db.add(fase_preparacion)
        self.db.commit()
        self.db.refresh(fase_preparacion)
        return fase_preparacion

    def get_fase_prueba(self, fase_id: int):
        return (
            self.db.query(FasePruebaModel)
            .filter(FasePruebaModel.id_fase == fase_id)
            .first()
        )

    def get_fase_preparacion(self, fase_id: int):
        return (
            self.db.query(FasePreparacionModel)
            .filter(FasePreparacionModel.id_fase == fase_id)
            .first()
        )
