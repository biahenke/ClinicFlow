from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db
from app.routers import auth, medicos, pacientes, consultas, users, especialidades, relatorios

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


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "ClinicFlow API running"}
