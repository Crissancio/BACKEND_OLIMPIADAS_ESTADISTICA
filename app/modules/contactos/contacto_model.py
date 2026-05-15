from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.db.database import Base


class ContactoModel(Base):
    __tablename__ = "contacto"

    id_contacto = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(100), nullable=False)
    correo_electronico = Column(String(150), nullable=False, index=True)
    asunto = Column(String(200), nullable=False)
    mensaje = Column(Text, nullable=False)
    estado = Column(String(20), nullable=False, server_default="PENDIENTE")
    creado_en = Column(DateTime, nullable=False, server_default=func.now(), index=True)
