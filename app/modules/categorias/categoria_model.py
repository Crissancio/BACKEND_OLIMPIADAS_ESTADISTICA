from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.database import Base


class CategoriaModel(Base):
    __tablename__ = "categoria"

    id_categoria = Column(Integer, primary_key=True, index=True)
    id_convocatoria = Column(Integer, ForeignKey("convocatoria.id_convocatoria"), nullable=False, index=True)
    nombre_categoria = Column(String(255), nullable=False)
    curso = Column(Integer, nullable=False)
    nivel = Column(String(20), nullable=False)
    estado = Column(String(20), nullable=False)
