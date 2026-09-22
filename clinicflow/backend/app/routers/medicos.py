from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from app.database import get_db
from app import models, schemas
from app.auth import get_password_hash
from app.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/medicos", tags=["Médicos"])


@router.get("/", response_model=schemas.MedicoList)
async def list_medicos(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db), 
    _=Depends(get_current_user)
):
    query = select(models.Medico)
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    
    return {"items": items, "total": total or 0}


@router.get("/{medico_id}", response_model=schemas.MedicoOut)
async def get_medico(medico_id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(models.Medico).where(models.Medico.id == medico_id))
    medico = result.scalar_one_or_none()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return medico


@router.post("/", response_model=schemas.MedicoOut, status_code=201)
async def create_medico(data: schemas.MedicoCreate, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    r = await db.execute(select(models.User).where(models.User.email == data.email))
    if r.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    r = await db.execute(select(models.Medico).where(models.Medico.crm == data.crm))
    if r.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="CRM já cadastrado")

    user = models.User(
        nome=data.nome,
        email=data.email,
        hashed_password=get_password_hash(data.password),
        role="medico"
    )
    db.add(user)
    await db.flush()

    medico = models.Medico(
        user_id=user.id,
        crm=data.crm,
        especialidade=data.especialidade,
        telefone=data.telefone
    )
    db.add(medico)
    await db.commit()
    await db.refresh(medico)
    await db.refresh(medico, attribute_names=["user"])
    return medico


@router.delete("/{medico_id}", status_code=204)
async def delete_medico(medico_id: int, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(models.Medico).where(models.Medico.id == medico_id))
    medico = result.scalar_one_or_none()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    await db.delete(medico)
    await db.commit()
