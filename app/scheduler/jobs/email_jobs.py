import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.modules.campanias.campania_model import CampaniaEmail, EstadoCampania, CampaniaDestinatario
from app.modules.email_logs.email_log_model import EmailLog, EstadoEmail, TipoEmail
from app.services.mailing.renderer import EmailRenderer
from app.services.mailing.sender import EmailSenderService

renderer = EmailRenderer()

def process_scheduled_campaigns():
    db: Session = SessionLocal()
    try:
        campanias = db.query(CampaniaEmail).filter(
            CampaniaEmail.estado == EstadoCampania.PROGRAMADA,
            CampaniaEmail.fecha_programada <= datetime.now()
        ).all()

        for camp in campanias:
            camp.estado = EstadoCampania.EN_PROCESO
            camp.fecha_inicio = datetime.now()
            
            destinatarios = db.query(CampaniaDestinatario).filter_by(id_campania=camp.id).all()
            
            for dest in destinatarios:
                html_content = renderer.render_campania(
                    asunto=camp.asunto,
                    usuario=dest.estudiante.nombres,
                    contenido_mensaje=camp.contenido_mensaje,
                    contenido_secundario=camp.contenido_secundario,
                    enlaces=camp.enlaces
                )
                
                log = EmailLog(
                    destinatario=dest.estudiante.correo,
                    asunto=camp.asunto,
                    contenido_html=html_content,
                    tipo=TipoEmail.MASIVO_INSCRIPCION,  # Tipo asignado 100% por backend
                    estado=EstadoEmail.PENDIENTE,
                    id_estudiante=dest.id_estudiante,
                    id_campania=camp.id
                )
                db.add(log)
            
            db.commit()
    finally:
        db.close()

async def send_pending_emails():
    db: Session = SessionLocal()
    try:
        sender_service = EmailSenderService(db)
        await sender_service.process_pending_emails()
    finally:
        db.close()

def finalize_campaigns():
    db: Session = SessionLocal()
    try:
        en_proceso = db.query(CampaniaEmail).filter(CampaniaEmail.estado == EstadoCampania.EN_PROCESO).all()
        
        for camp in en_proceso:
            pendientes = db.query(EmailLog).filter(
                EmailLog.id_campania == camp.id,
                EmailLog.estado.in_([EstadoEmail.PENDIENTE, EstadoEmail.EN_PROCESO])
            ).count()
            
            if pendientes == 0:
                camp.estado = EstadoCampania.FINALIZADA
                camp.fecha_fin = datetime.now()
        
        db.commit()
    finally:
        db.close()