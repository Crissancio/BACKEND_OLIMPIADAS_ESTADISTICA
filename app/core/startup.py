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
                nombre=settings.first_admin_username,
                correo=settings.first_admin_email,
                contrasena=hash_password(
                    settings.first_admin_password
                )
            )

            db.add(admin)
            db.commit()
            logger.info(f"Administrador inicial creado correctamente. {admin.nombre}")
        
        logger.info(
                "Administrador inicial ya existe"
            )
    finally:
        db.close()