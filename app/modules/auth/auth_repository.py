from sqlalchemy.orm import Session

from app.modules.auth.auth_model import AdministradorModel, AuditoriaModel


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_admin_by_id(self, admin_id: int):
        return (
            self.db.query(AdministradorModel)
            .filter(AdministradorModel.id_administrador == admin_id)
            .first()
        )

    def get_admin_by_correo(self, correo: str):
        return self.db.query(AdministradorModel).filter(AdministradorModel.correo == correo).first()

    def count_admins(self):
        return self.db.query(AdministradorModel).count()

    def create_admin(self, admin: AdministradorModel):
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return admin

    def create_auditoria(self, admin_id: int, accion: str, descripcion: str | None = None):
        auditoria = AuditoriaModel(
            id_administrador=admin_id,
            accion=accion,
            descripcion=descripcion,
        )
        self.db.add(auditoria)
        self.db.commit()
        self.db.refresh(auditoria)
        return auditoria
