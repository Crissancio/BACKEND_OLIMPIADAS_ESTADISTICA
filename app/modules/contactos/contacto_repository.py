from sqlalchemy.orm import Session

from app.modules.contactos.contacto_model import ContactoModel


class ContactoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, contacto_id: int):
        return self.db.query(ContactoModel).filter(ContactoModel.id_contacto == contacto_id).first()

    def get_all(self, skip: int, limit: int, correo_electronico: str | None = None, estado: str | None = None):
        query = self.db.query(ContactoModel)
        if correo_electronico:
            query = query.filter(ContactoModel.correo_electronico.ilike(f"%{correo_electronico}%"))
        if estado:
            query = query.filter(ContactoModel.estado == estado)
        return query.order_by(ContactoModel.creado_en.desc()).offset(skip).limit(limit).all()

    def count_all(self, correo_electronico: str | None = None, estado: str | None = None):
        query = self.db.query(ContactoModel)
        if correo_electronico:
            query = query.filter(ContactoModel.correo_electronico.ilike(f"%{correo_electronico}%"))
        if estado:
            query = query.filter(ContactoModel.estado == estado)
        return query.count()

    def create(self, contacto: ContactoModel):
        self.db.add(contacto)
        self.db.commit()
        self.db.refresh(contacto)
        return contacto

    def update(self, contacto: ContactoModel):
        self.db.commit()
        self.db.refresh(contacto)
        return contacto

    def delete(self, contacto: ContactoModel):
        self.db.delete(contacto)
        self.db.commit()
