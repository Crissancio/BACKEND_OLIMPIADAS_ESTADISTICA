from sqlalchemy.orm import Session

from app.modules.convocatorias.convocatoria_model import ConvocatoriaModel


class ConvocatoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, convocatoria_id: int):
        return (
            self.db.query(ConvocatoriaModel)
            .filter(ConvocatoriaModel.id_convocatoria == convocatoria_id)
            .first()
        )

    def get_all(self, skip: int, limit: int):
        return self.db.query(ConvocatoriaModel).offset(skip).limit(limit).all()

    def count_all(self):
        return self.db.query(ConvocatoriaModel).count()

    def create(self, convocatoria: ConvocatoriaModel):
        self.db.add(convocatoria)
        self.db.commit()
        self.db.refresh(convocatoria)
        return convocatoria

    def update(self, convocatoria: ConvocatoriaModel):
        self.db.commit()
        self.db.refresh(convocatoria)
        return convocatoria

    def delete(self, convocatoria: ConvocatoriaModel):
        self.db.delete(convocatoria)
        self.db.commit()

    def get_active(self):
        return (
            self.db.query(ConvocatoriaModel)
            .filter(
                ConvocatoriaModel.estado.in_(
                    ["ACTIVA", "PROXIMA", "FINALIZADA", "INSCRIPCION EN CURSO"]
                )
            )
            .order_by(ConvocatoriaModel.id_convocatoria.desc())
            .first()
        )

    def get_last_finalizada(self):
        return (
            self.db.query(ConvocatoriaModel)
            .filter(ConvocatoriaModel.estado == "FINALIZADA")
            .order_by(ConvocatoriaModel.fin_olimpiadas.desc())
            .first()
        )
