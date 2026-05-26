from sqlalchemy.orm import Session

from app.modules.auth.auth_model import AdministradorModel


class AdministradorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, administrador_id: int):
        return (
            self.db.query(AdministradorModel)
            .filter(AdministradorModel.id_administrador == administrador_id)
            .first()
        )

    def get_by_correo(self, correo: str):
        return self.db.query(AdministradorModel).filter(AdministradorModel.correo == correo).first()

    def get_all(self, skip: int, limit: int, nombre: str | None = None, correo: str | None = None):
        query = self._apply_filters(nombre=nombre, correo=correo)
        return query.offset(skip).limit(limit).all()

    def count_all(self, nombre: str | None = None, correo: str | None = None):
        return self._apply_filters(nombre=nombre, correo=correo).count()

    def create(self, administrador: AdministradorModel):
        self.db.add(administrador)
        self.db.commit()
        self.db.refresh(administrador)
        return administrador

    def update(self, administrador: AdministradorModel):
        self.db.commit()
        self.db.refresh(administrador)
        return administrador

    def delete(self, administrador: AdministradorModel):
        self.db.delete(administrador)
        self.db.commit()

    def _apply_filters(self, nombre: str | None = None, correo: str | None = None):
        query = self.db.query(AdministradorModel)
        if nombre:
            query = query.filter(AdministradorModel.nombre.ilike(f"%{nombre}%"))
        if correo:
            query = query.filter(AdministradorModel.correo.ilike(f"%{correo}%"))
        return query
