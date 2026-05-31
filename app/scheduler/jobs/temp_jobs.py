import logging
import shutil
from pathlib import Path

from app.core.config import settings

logger = logging.getLogger(__name__)


def cleanup_temp_directory():
    base_dir = Path.cwd()
    temp_dir = Path(settings.temp_cleanup_dir)
    if not temp_dir.is_absolute():
        temp_dir = base_dir / temp_dir

    temp_dir = temp_dir.resolve()
    protected_paths = {base_dir.resolve(), Path(temp_dir.anchor).resolve()}
    if temp_dir in protected_paths:
        logger.error("Limpieza de temp cancelada: ruta insegura %s", temp_dir)
        return

    temp_dir.mkdir(parents=True, exist_ok=True)
    deleted = 0

    for item in temp_dir.iterdir():
        try:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
            deleted += 1
        except Exception:
            logger.exception("No se pudo eliminar item temporal: %s", item)

    logger.info("Limpieza de temp completada: %s items eliminados en %s", deleted, temp_dir)
