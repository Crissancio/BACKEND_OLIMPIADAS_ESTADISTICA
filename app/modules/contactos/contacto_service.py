from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.modules.auth.auth_repository import AuthRepository
from app.modules.contactos.contacto_model import ContactoModel
from app.modules.contactos.contacto_repository import ContactoRepository
from app.modules.contactos.contacto_schema import ContactoCreateDTO, ContactoUpdateDTO


ESTADOS_CONTACTO = {"PENDIENTE", "RESPONDIDO", "LEIDO"}


class ContactoService:
    def __init__(self, db: Session):
        self.repository = ContactoRepository(db)
        self.auth_repository = AuthRepository(db)

    def get_by_id(self, contacto_id: int):
        contacto = self.repository.get_by_id(contacto_id)
        if not contacto:
            raise NotFoundError("Mensaje de contacto no encontrado")
        return contacto

    def get_all(self, page: int, limit: int, correo_electronico: str | None = None, estado: str | None = None):
        if estado is not None:
            self._validar_estado(estado)
        skip = (page - 1) * limit
        items = self.repository.get_all(skip=skip, limit=limit, correo_electronico=correo_electronico, estado=estado)
        total = self.repository.count_all(correo_electronico=correo_electronico, estado=estado)
        return items, total

    def create(self, data: ContactoCreateDTO):
        contacto = ContactoModel(**data.model_dump(), estado="PENDIENTE")
        return self.repository.create(contacto)

    def update(self, contacto_id: int, data: ContactoUpdateDTO, current_admin_id: int):
        self._validar_estado(data.estado)
        contacto = self.get_by_id(contacto_id)
        contacto.estado = data.estado
        updated = self.repository.update(contacto)
        self.auth_repository.create_auditoria(
            admin_id=current_admin_id,
            accion="ACTUALIZAR_CONTACTO",
            descripcion=f"Estado contacto {updated.id_contacto}: {updated.estado}",
        )
        return updated

    def delete(self, contacto_id: int, current_admin_id: int):
        contacto = self.get_by_id(contacto_id)
        deleted = {
            "id_contacto": contacto.id_contacto,
            "nombre_completo": contacto.nombre_completo,
            "correo_electronico": contacto.correo_electronico,
            "asunto": contacto.asunto,
            "mensaje": contacto.mensaje,
            "estado": contacto.estado,
            "creado_en": contacto.creado_en,
        }
        self.repository.delete(contacto)
        self.auth_repository.create_auditoria(
            admin_id=current_admin_id,
            accion="ELIMINAR_CONTACTO",
            descripcion=f"Mensaje de contacto eliminado: {deleted['correo_electronico']}",
        )
        return deleted

    def _validar_estado(self, estado: str):
        if estado not in ESTADOS_CONTACTO:
            raise BusinessRuleError("Estado de contacto invalido")
