import enum

from sqlalchemy import Column, Enum, Integer, String

from app.db.database import Base


class EstadoAdministrador(str, enum.Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"


class AdministradorModel(Base):
    __tablename__ = "administrador"

    id_administrador = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    correo = Column(String(255), nullable=False, unique=True, index=True)
    contrasena = Column(String(255), nullable=False)
    estado = Column(Enum(EstadoAdministrador, name="estado_administrador"), nullable=False, default=EstadoAdministrador.ACTIVO)
