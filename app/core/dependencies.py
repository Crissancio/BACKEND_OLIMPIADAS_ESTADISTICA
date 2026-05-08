from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedError
from app.core.security import decode_access_token
from app.db.database import get_db
from app.modules.auth.auth_repository import AuthRepository


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> int:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedError("No autorizado")

    payload = decode_access_token(credentials.credentials)
    admin_id = payload.get("sub")
    if admin_id is None:
        raise UnauthorizedError("Token invalido")

    repository = AuthRepository(db)
    admin = repository.get_admin_by_id(int(admin_id))
    if not admin:
        raise UnauthorizedError("No autorizado")

    return admin.id_administrador
