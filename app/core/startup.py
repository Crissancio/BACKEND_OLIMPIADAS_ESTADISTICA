from app.db.database import SessionLocal
from app.modules.auth.auth_model import AdministradorModel
from app.core.config import settings
from app.core.security import hash_password
import logging

logger = logging.getLogger(__name__)

def create_initial_admin():
    db = SessionLocal()

    try:
        admin_exists = db.query(AdministradorModel).first()

        if not admin_exists:
            admin = AdministradorModel(
                username=settings.FIRST_ADMIN_USERNAME,
                correo=settings.FIRST_ADMIN_EMAIL,
                password_hash=hash_password(
                    settings.FIRST_ADMIN_PASSWORD
                )
            )

            db.add(admin)
            db.commit()
            logger.info(f"Administrador inicial creado correctamente. {admin.username}")
        
        logger.info(
                "Administrador inicial ya existe"
            )
    finally:
        db.close()