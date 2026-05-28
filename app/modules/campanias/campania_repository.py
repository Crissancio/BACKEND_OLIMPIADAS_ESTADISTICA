from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional
from datetime import datetime
from app.modules.campanias.campania_model import CampaniaEmail, CampaniaDestinatario

class CampaniaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int, limit: int, nombre: Optional[str], asunto: Optional[str], estado: Optional[str],
                creacion_start: Optional[datetime], creacion_end: Optional[datetime],
                prog_start: Optional[datetime], prog_end: Optional[datetime],
                inicio_start: Optional[datetime], inicio_end: Optional[datetime],
                fin_start: Optional[datetime], fin_end: Optional[datetime]):
        
        query = self.db.query(CampaniaEmail)
        
        if nombre:
            query = query.filter(CampaniaEmail.nombre.ilike(f"%{nombre}%"))
        if asunto:
            query = query.filter(CampaniaEmail.asunto.ilike(f"%{asunto}%"))
        if estado:
            query = query.filter(CampaniaEmail.estado == estado)
            
        if creacion_start and creacion_end: query = query.filter(CampaniaEmail.fecha_creacion.between(creacion_start, creacion_end))
        if prog_start and prog_end: query = query.filter(CampaniaEmail.fecha_programada.between(prog_start, prog_end))
        if inicio_start and inicio_end: query = query.filter(CampaniaEmail.fecha_inicio.between(inicio_start, inicio_end))
        if fin_start and fin_end: query = query.filter(CampaniaEmail.fecha_fin.between(fin_start, fin_end))
        
        total = query.count()
        items = query.order_by(CampaniaEmail.fecha_creacion.desc()).offset(skip).limit(limit).all()
        return items, total

    def get_by_id(self, id_campania: int) -> CampaniaEmail:
        return self.db.query(CampaniaEmail).filter(CampaniaEmail.id == id_campania).first()

    def delete(self, id_campania: int):
        campania = self.get_by_id(id_campania)
        if campania:
            self.db.delete(campania)
            self.db.commit()