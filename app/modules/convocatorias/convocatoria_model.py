from sqlalchemy import Column, Date, DateTime, Integer, Numeric, String, Text

from app.db.database import Base


class ConvocatoriaModel(Base):
    __tablename__ = "convocatoria"

    id_convocatoria = Column(Integer, primary_key=True, index=True)
    nombre_convocatoria = Column(String(255), nullable=False)
    gestion = Column(Integer, nullable=False)
    descripcion = Column(Text, nullable=True)
    inicio_olimpiadas = Column(Date, nullable=True)
    fin_olimpiadas = Column(Date, nullable=True)
    fecha_inicio_inscripcion = Column(DateTime, nullable=True)
    fecha_fin_inscripcion = Column(DateTime, nullable=True)
    monto_inscripcion = Column(Numeric(10, 2), nullable=True)
    estado = Column(String(20), nullable=False)
