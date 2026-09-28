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
    # Assegurar que atendimentos futuros no banco não estejam marcados como realizada
    try:
        from .database import AsyncSessionLocal
        from .models import Consulta
        from sqlalchemy import select, or_, and_
        from datetime import date, datetime
        async with AsyncSessionLocal() as session:
            hoje = date.today()
            agora = datetime.now().time()
            query = select(Consulta).where(
                or_(
                    Consulta.status.ilike('realizada'),
                    Consulta.status.ilike('realizado')
                ),
                or_(
                    Consulta.data > hoje,
                    and_(Consulta.data == hoje, Consulta.horario > agora)
                )
            )
            result = await session.execute(query)
            futuras_realizadas = result.scalars().all()
            if futuras_realizadas:
                for c in futuras_realizadas:
                    c.status = 'agendada'
                await session.commit()
                print(f'[INFO] {len(futuras_realizadas)} atendimentos futuros corrigidos de realizada para agendada.')
    except Exception as e:
        print(f'[WARN] Erro ao sanitizar status de consultas futuras na inicializacao: {e}')
    yield

app = FastAPI(
    title="ClinicFlow API",
    description="Sistema de gestão de clínicas médicas",
    version="1.0.0",
    lifespan=lifespan
)

# ✅ CORS MIDDLEWARE COM DECORATOR
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Serve frontend static files (HTML, CSS, JS)
import os
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))

app.include_router(auth.router, prefix="/api")
app.include_router(medicos.router, prefix="/api")
app.include_router(pacientes.router, prefix="/api")
app.include_router(consultas.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(especialidades.router, prefix="/api")
app.include_router(relatorios.router, prefix="/api")
@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "message": "ClinicFlow API running"}

# Debug endpoint to show frontend path
@app.get("/debug_path", tags=["Debug"])
async def debug_path():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))
    exists = os.path.isdir(path)
    return {"frontend_path": path, "exists": exists}

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
