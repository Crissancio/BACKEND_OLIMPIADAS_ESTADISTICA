from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.core.security import hash_password
from app.modules.administradores.administrador_repository import AdministradorRepository
from app.modules.administradores.administrador_schema import (
    AdministradorCreateDTO,
    AdministradorUpdateDTO,
)
from app.modules.auth.auth_model import AdministradorModel


class AdministradorService:
    def __init__(self, db: Session):
        self.repository = AdministradorRepository(db)

    def get_by_id(self, administrador_id: int):
        administrador = self.repository.get_by_id(administrador_id)
        if not administrador:
            raise NotFoundError("Administrador no encontrado")
        return administrador

    def get_all(self, page: int, limit: int, nombre: str | None = None, correo: str | None = None):
        skip = (page - 1) * limit
        items = self.repository.get_all(skip=skip, limit=limit, nombre=nombre, correo=correo)
        total = self.repository.count_all(nombre=nombre, correo=correo)
        return items, total

    def create(self, data: AdministradorCreateDTO):
        self._validate_password(data.contrasena)
        if self.repository.get_by_correo(data.correo):
            raise ConflictError("El correo ya esta registrado")

        administrador = AdministradorModel(
            nombre=data.nombre,
            correo=data.correo,
            contrasena=hash_password(data.contrasena),
            estado="ACTIVO",
        )
        return self.repository.create(administrador)

    def update(self, administrador_id: int, data: AdministradorUpdateDTO):
        administrador = self.get_by_id(administrador_id)
        updates = data.model_dump(exclude_unset=True)

        if "correo" in updates and updates["correo"] != administrador.correo:
            existing = self.repository.get_by_correo(updates["correo"])
            if existing:
                raise ConflictError("El correo ya esta registrado")

        for key, value in updates.items():
            setattr(administrador, key, value)

        return self.repository.update(administrador)

    def delete_total(self, administrador_id: int):
        administrador = self.get_by_id(administrador_id)
        data = {
            "id_administrador": administrador.id_administrador,
            "nombre": administrador.nombre,
            "correo": administrador.correo,
            "estado": administrador.estado,
        }
        self.repository.delete(administrador)
        return data

    def baja_logic(self, administrador_id: int):
        administrador = self.get_by_id(administrador_id)
        administrador.estado = "INACTIVO"
        return self.repository.update(administrador)

    def alta_logic(self, administrador_id: int):
        administrador = self.get_by_id(administrador_id)
        administrador.estado = "ACTIVO"
        return self.repository.update(administrador)

    def _validate_password(self, contrasena: str):
        if len(contrasena) < 8:
            raise ValidationError("La contrasena debe tener al menos 8 caracteres")
