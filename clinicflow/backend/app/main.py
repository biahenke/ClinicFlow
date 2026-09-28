from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from contextlib import asynccontextmanager
from .database import init_db
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .routers import auth, medicos, pacientes, consultas, users, especialidades, relatorios

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria todas as tabelas na inicialização
    await init_db()
    yield

app = FastAPI(
    title="ClinicFlow API",
    description="Sistema de gestão de clínicas médicas",
    version="1.0.0",
    lifespan=lifespan
)

# Serve frontend static files (HTML, CSS, JS)
import os
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))
# Static files will be mounted after routers (see below)

# CORS — permite frontend (porta 3000) acessar o backend (porta 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(medicos.router, prefix="/api")
app.include_router(pacientes.router, prefix="/api")
app.include_router(consultas.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(especialidades.router, prefix="/api")
app.include_router(relatorios.router, prefix="/api")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/", response_class=HTMLResponse)
async def root():
    import os
    index_path = os.path.join(frontend_path, "index.html")
    return FileResponse(index_path, media_type="text/html")


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "message": "ClinicFlow API running"}

# Debug endpoint to show frontend path
@app.get("/debug_path", tags=["Debug"])
async def debug_path():
    import os
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))
    exists = os.path.isdir(path)
    return {"frontend_path": path, "exists": exists}
