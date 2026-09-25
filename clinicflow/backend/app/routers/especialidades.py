from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct
from typing import List
from app.database import get_db
from app import models

router = APIRouter(prefix="/especialidades", tags=["Especialidades"])

DEFAULT_ESPECIALIDADES = [
    "Cardiologia",
    "Cirurgia Geral",
    "Clínica Geral",
    "Dermatologia",
    "Endocrinologia",
    "Gastroenterologia",
    "Geriatria",
    "Ginecologia",
    "Neurologia",
    "Oftalmologia",
    "Ortopedia",
    "Otorrinolaringologia",
    "Pediatria",
    "Pneumologia",
    "Psiquiatria",
    "Urologia"
]

@router.get("/", response_model=List[str])
async def list_especialidades(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(distinct(models.Medico.especialidade)))
    db_especialidades = [r for r in result.scalars().all() if r]
    
    # Merge predefined + any existing in DB, unique and sorted
    all_esp = sorted(list(set(DEFAULT_ESPECIALIDADES + db_especialidades)))
    return all_esp
