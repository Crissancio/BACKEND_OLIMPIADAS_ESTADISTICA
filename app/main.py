from fastapi import FastAPI

from app.core.exceptions import register_exception_handlers
from app.modules.auth.auth_router import router as auth_router
from app.modules.categorias.categoria_router import router as categoria_router
from app.modules.colegios.colegio_router import router as colegio_router
from app.modules.convocatorias.convocatoria_router import router as convocatoria_router
from app.modules.fases.fase_router import router as fase_router
from app.modules.personas.persona_router import router as persona_router


app = FastAPI()
register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(convocatoria_router)
app.include_router(categoria_router)
app.include_router(colegio_router)
app.include_router(fase_router)
app.include_router(persona_router)
