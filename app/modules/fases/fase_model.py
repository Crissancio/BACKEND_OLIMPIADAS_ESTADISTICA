from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.db.database import Base


class FaseModel(Base):
    __tablename__ = "fase"

    id_fase = Column(Integer, primary_key=True, index=True)
    id_categoria_fk = Column(Integer, ForeignKey("categoria.id_categoria"), nullable=False, index=True)
    nombre_fase = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    modalidad = Column(String(20), nullable=False)
    estado = Column(String(20), nullable=False)


class FasePruebaModel(Base):
    __tablename__ = "fase_prueba"

    id_fase = Column(Integer, ForeignKey("fase.id_fase"), primary_key=True, index=True)
    id_fase_anterior = Column(Integer, ForeignKey("fase_prueba.id_fase"), nullable=True)
    criterio_aprobacion = Column(Integer, nullable=False)
    fecha_realizacion = Column(DateTime, nullable=False)
    lugar_realizacion = Column(String(255), nullable=True)


class FasePreparacionModel(Base):
    __tablename__ = "fase_preparacion"

    id_fase = Column(Integer, ForeignKey("fase.id_fase"), primary_key=True, index=True)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
