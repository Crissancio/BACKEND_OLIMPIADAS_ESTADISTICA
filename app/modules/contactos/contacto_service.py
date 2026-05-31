from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError, BusinessRuleError
from app.modules.contactos.contacto_model import ContactoModel, EstadoContacto
from app.modules.contactos.contacto_repository import ContactoRepository
from app.modules.contactos.contacto_schema import ContactoCreateDTO, ContactoRespuestaCreateDTO
from app.modules.email_logs.email_log_model import EmailLog, EstadoEmail, TipoEmail
from app.services.mailing.renderer import EmailRenderer
from app.modules.sistema.sistema_repository import SistemaRepository
from app.modules.sistema.sistema_model import ActividadSistemaModel, AuditoriaModel, TipoAccion, TipoModulo, TipoActividad
class ContactoService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ContactoRepository(db)
        self.sistema_repository = SistemaRepository(db)
        self.renderer = EmailRenderer()

    def get_by_id(self, contacto_id: int):
        contacto = self.repository.get_by_id(contacto_id)
        if not contacto:
            raise NotFoundError("Mensaje de contacto no encontrado")
        return contacto

    def get_all(self, page: int, limit: int, **filters):
        skip = (page - 1) * limit
        return self.repository.get_all(skip=skip, limit=limit, **filters)

    def get_all_respondidos(self, page: int, limit: int, **filters):
        skip = (page - 1) * limit
        return self.repository.get_all_respondidos(skip=skip, limit=limit, **filters)

    def create(self, data: ContactoCreateDTO):
        contacto = ContactoModel(
            nombre_completo=data.nombre_completo,
            correo_electronico=data.correo_electronico,
            asunto=data.asunto,
            mensaje=data.mensaje,
            estado=EstadoContacto.PENDIENTE
        )
        
        actividad_registro = ActividadSistemaModel(
            tipo=TipoActividad.EMAIL,
            titulo="Creación de Contacto",
            descripcion=f"Se creó un nuevo mensaje de contacto de {contacto.nombre_completo} con asunto {contacto.asunto}"
        )
        
        self.sistema_repository.create_actividad(actividad_registro)
        return self.repository.create(contacto)

    def marcar_leido(self, contacto_id: int, current_admin_id: int):
        contacto = self.get_by_id(contacto_id)
        if contacto.estado != EstadoContacto.PENDIENTE:
            raise BusinessRuleError("Solo se pueden marcar como leídos los contactos PENDIENTES")
            
        contacto.estado = EstadoContacto.LEIDO
        self.repository.update()
        self.db.refresh(contacto)
        auditoria_registro = AuditoriaModel(
            id_administrador=current_admin_id,
            accion=TipoAccion.ACTUALIZAR,
            modulo=TipoModulo.CONTACTO,
            descripcion=f"Contacto {contacto.nombre_completo} {contacto.correo_electronico} marcado como leído"
        )
        self.sistema_repository.create_auditoria(auditoria_registro)
        return contacto

    def responder(self, contacto_id: int, data: ContactoRespuestaCreateDTO, current_admin_id: int):
        contacto = self.get_by_id(contacto_id)
        if contacto.estado == EstadoContacto.RESPONDIDO:
            raise BusinessRuleError("Este contacto ya ha sido respondido")

        dict_enlaces = [e.model_dump() for e in data.enlaces] if data.enlaces else []

        html_content = self.renderer.render_respuesta_contacto(
            asunto_correo=data.asunto_correo,
            usuario=contacto.nombre_completo,
            asunto_original=contacto.asunto,
            contenido_mensaje=data.contenido_mensaje,
            contenido_secundario=data.contenido_secundario,
            enlaces=dict_enlaces
        )

        email_log = EmailLog(
            destinatario=contacto.correo_electronico,
            asunto=data.asunto_correo,
            contenido_html=html_content,
            tipo=TipoEmail.RESPUESTA_CONTACTO,
            estado=EstadoEmail.PENDIENTE,
            id_contacto=contacto.id_contacto
        )
        self.db.add(email_log)
        
        contacto.estado = EstadoContacto.RESPONDIDO
        self.repository.update()
        self.db.refresh(contacto)
        
        auditoria_registro = AuditoriaModel(
            id_administrador=current_admin_id,
            accion=TipoAccion.RESPONDER,
            modulo=TipoModulo.CONTACTO,
            descripcion=f"Contacto {contacto.nombre_completo} {contacto.correo_electronico} respondido"
        )
        self.sistema_repository.create_auditoria(auditoria_registro)
        
        return contacto

    def delete(self, contacto_id: int, current_admin_id: int):
        contacto = self.get_by_id(contacto_id)
        self.repository.delete(contacto)
        auditoria_registro = AuditoriaModel(
            id_administrador=current_admin_id,
            accion=TipoAccion.ELIMINAR,
            modulo=TipoModulo.CONTACTO,
            descripcion=f"Contacto {contacto.nombre_completo} {contacto.correo_electronico} eliminado"
        )
        self.sistema_repository.create_auditoria(auditoria_registro)
        return None