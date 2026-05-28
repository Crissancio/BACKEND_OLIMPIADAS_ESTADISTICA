from sqlalchemy.orm import Session
from datetime import datetime
from app.core.exceptions import BusinessRuleError, NotFoundError
from app.modules.campanias.campania_model import CampaniaEmail, EstadoCampania, CampaniaDestinatario
from app.modules.campanias.campania_schema import CampaniaCreateDTO, CampaniaUpdateDTO
from app.modules.campanias.campania_repository import CampaniaRepository

class CampaniaService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CampaniaRepository(db)

    def listar_campanias(self, page: int, limit: int, **filters):
        skip = (page - 1) * limit
        items, total = self.repo.get_all(skip=skip, limit=limit, **filters)
        return items, total

    def obtener_por_id(self, id_campania: int):
        campania = self.repo.get_by_id(id_campania)
        if not campania:
            raise NotFoundError("Campaña no encontrada")
        return campania

    def crear_campania(self, data: CampaniaCreateDTO) -> CampaniaEmail:
        dict_enlaces = [e.model_dump() for e in data.enlaces] if data.enlaces else []
        nueva = CampaniaEmail(
            nombre=data.nombre,
            asunto=data.asunto,
            contenido_mensaje=data.contenido_mensaje,
            contenido_secundario=data.contenido_secundario,
            enlaces=dict_enlaces,
            fecha_programada=data.fecha_programada,
            estado=EstadoCampania.BORRADOR
        )
        self.db.add(nueva)
        self.db.commit()
        self.db.refresh(nueva)

        if data.destinatarios_ids:
            self._gestionar_destinatarios(nueva.id, agregar=data.destinatarios_ids)
            
        return nueva

    def actualizar_campania(self, id_campania: int, data: CampaniaUpdateDTO) -> CampaniaEmail:
        campania = self.obtener_por_id(id_campania)
        
        if campania.estado != EstadoCampania.BORRADOR:
            raise BusinessRuleError("Solo se pueden editar campañas en estado BORRADOR")

        if data.nombre: campania.nombre = data.nombre
        if data.asunto: campania.asunto = data.asunto
        if data.contenido_mensaje: campania.contenido_mensaje = data.contenido_mensaje
        if data.contenido_secundario: campania.contenido_secundario = data.contenido_secundario
        if data.enlaces is not None: campania.enlaces = [e.model_dump() for e in data.enlaces]
        if data.fecha_programada: campania.fecha_programada = data.fecha_programada

        if data.agregar_destinatarios or data.eliminar_destinatarios:
            self._gestionar_destinatarios(campania.id, data.agregar_destinatarios, data.eliminar_destinatarios)

        self.db.commit()
        self.db.refresh(campania)
        return campania

    def cambiar_estado(self, id_campania: int, nuevo_estado: EstadoCampania):
        campania = self.obtener_por_id(id_campania)

        if nuevo_estado == EstadoCampania.PROGRAMADA:
            if campania.estado not in (EstadoCampania.BORRADOR, EstadoCampania.CANCELADA):
                raise BusinessRuleError("Solo se puede programar desde BORRADOR o CANCELADA")
            total_dest = self.db.query(CampaniaDestinatario).filter_by(id_campania=id_campania).count()
            if total_dest == 0:
                raise BusinessRuleError("No se puede programar una campaña sin destinatarios")
                
        elif nuevo_estado == EstadoCampania.CANCELADA:
            if campania.estado not in (EstadoCampania.PROGRAMADA, EstadoCampania.EN_PROCESO):
                raise BusinessRuleError("Solo se puede cancelar una campaña PROGRAMADA o EN_PROCESO")
        
        elif nuevo_estado == EstadoCampania.BORRADOR:
             raise BusinessRuleError("No se puede regresar una campaña a BORRADOR manualmente")

        campania.estado = nuevo_estado
        self.db.commit()
        self.db.refresh(campania)
        return campania

    def eliminar_campania(self, id_campania: int):
        campania = self.obtener_por_id(id_campania)
        self.repo.delete(id_campania)
        return campania

    def _gestionar_destinatarios(self, id_campania: int, agregar: list = None, eliminar: list = None):
        if eliminar:
            self.db.query(CampaniaDestinatario).filter(
                CampaniaDestinatario.id_campania == id_campania,
                CampaniaDestinatario.id_estudiante.in_(eliminar)
            ).delete(synchronize_session=False)
        
        if agregar:
            existentes = self.db.query(CampaniaDestinatario.id_estudiante).filter(
                CampaniaDestinatario.id_campania == id_campania,
                CampaniaDestinatario.id_estudiante.in_(agregar)
            ).all()
            existentes_ids = [e[0] for e in existentes]
            
            nuevos = [
                CampaniaDestinatario(id_campania=id_campania, id_estudiante=est_id) 
                for est_id in agregar if est_id not in existentes_ids
            ]
            if nuevos:
                self.db.bulk_save_objects(nuevos)