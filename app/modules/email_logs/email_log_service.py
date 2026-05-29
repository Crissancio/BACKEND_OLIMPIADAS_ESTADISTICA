from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError
from app.modules.email_logs.email_log_repository import EmailLogRepository
from app.modules.email_logs.email_log_model import EstadoEmail, EmailLog
from app.core.exceptions import BusinessRuleError
class EmailLogService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = EmailLogRepository(db)

    def listar_logs(self, page: int, limit: int, **filters):
        skip = (page - 1) * limit
        return self.repo.get_all(skip=skip, limit=limit, **filters)

    def obtener_por_id(self, id_log: int):
        log = self.repo.get_by_id(id_log)
        if not log:
            raise NotFoundError("Log de email no encontrado")
        return log

    def reintentar_fallidos(self):
        fallidos = self.db.query(EmailLog).filter(EmailLog.estado == EstadoEmail.FALLIDO).all()
        for log in fallidos:
            log.estado = EstadoEmail.PENDIENTE
        self.db.commit()
        return len(fallidos)
    
    def reintentar_fallido(self, id_log: int):
        log = self.obtener_por_id(id_log)
        if log.estado != EstadoEmail.FALLIDO:
            raise BusinessRuleError("El correo especificado no está en estado FALLIDO")
        
        log.estado = EstadoEmail.PENDIENTE
        log.intentos = 0
        self.db.commit()
        self.db.refresh(log)
        return log