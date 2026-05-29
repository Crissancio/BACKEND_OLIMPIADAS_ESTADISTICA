import enum
from sqlalchemy import CheckConstraint, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class NivelEducativo(str, enum.Enum):
    PRIMARIA = 'PRIMARIA'
    SECUNDARIA = 'SECUNDARIA'

class EstadoEntidad(str, enum.Enum):
    BORRADOR = 'BORRADOR'
    LISTA = 'LISTA'
    ELIMINADA = 'ELIMINADA'

class CategoriaModel(Base):
    __tablename__ = "categoria"

    id_categoria = Column(Integer, primary_key=True, index=True)
    id_convocatoria = Column(Integer, ForeignKey("convocatoria.id_convocatoria", ondelete="CASCADE"), nullable=False, index=True)
    nombre_categoria = Column(String(255), nullable=False)
    curso = Column(Integer, nullable=False)
    nivel = Column(Enum(NivelEducativo, name="nivel_educativo"), nullable=False)
    estado = Column(Enum(EstadoEntidad, name="estado_entidad"), nullable=False, default=EstadoEntidad.BORRADOR)

    __table_args__ = (
        CheckConstraint('curso BETWEEN 1 AND 6', name='check_curso_rango'),
    )

    fases = relationship("FaseModel", back_populates="categoria", cascade="all, delete")
    inscripciones = relationship("InscripcionModel", back_populates="categoria")