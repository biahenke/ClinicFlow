from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import select, func
from typing import List
from app.database import get_db
from app import models, schemas
from app.auth import get_password_hash
from app.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.get("/", response_model=schemas.PacienteList)
async def list_pacientes(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db), 
    _=Depends(get_current_user)
):
    query = select(models.Paciente)
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    
    return {"items": items, "total": total or 0}


@router.get("/{paciente_id}", response_model=schemas.PacienteOut)
async def get_paciente(paciente_id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(models.Paciente).where(models.Paciente.id == paciente_id))
    paciente = result.scalar_one_or_none()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente


@router.post("/", response_model=schemas.PacienteOut, status_code=201)
async def create_paciente(data: schemas.PacienteCreate, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    r = await db.execute(select(models.User).where(models.User.email == data.email))
    if r.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    r = await db.execute(select(models.Paciente).where(models.Paciente.cpf == data.cpf))
    if r.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    user = models.User(
        nome=data.nome,
        email=data.email,
        hashed_password=get_password_hash(data.password),
        role="paciente"
    )
    db.add(user)
    await db.flush()

    paciente = models.Paciente(
        user_id=user.id,
        cpf=data.cpf,
        data_nascimento=data.data_nascimento,
        telefone=data.telefone,
        endereco=data.endereco,
        genero=data.genero
    )
    db.add(paciente)
    await db.commit()
    await db.refresh(paciente)
    await db.refresh(paciente, attribute_names=["user"])
    return paciente



@router.put("/{paciente_id}", response_model=schemas.PacienteOut)
async def update_paciente(paciente_id: int, data: schemas.PacienteUpdate, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(models.Paciente).where(models.Paciente.id == paciente_id))
    paciente = result.scalar_one_or_none()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Update User info
    if data.nome is not None or data.email is not None:
        user_result = await db.execute(select(models.User).where(models.User.id == paciente.user_id))
        user = user_result.scalar_one_or_none()
        if user:
            if data.nome is not None:
                user.nome = data.nome
            if data.email is not None:
                # check if email exists
                if data.email != user.email:
                    email_check = await db.execute(select(models.User).where(models.User.email == data.email))
                    if email_check.scalar_one_or_none():
                        raise HTTPException(status_code=400, detail="Email já cadastrado")
                user.email = data.email

    if data.cpf is not None:
        # check if cpf exists
        if data.cpf != paciente.cpf:
            cpf_check = await db.execute(select(models.Paciente).where(models.Paciente.cpf == data.cpf))
            if cpf_check.scalar_one_or_none():
                raise HTTPException(status_code=400, detail="CPF já cadastrado")
        paciente.cpf = data.cpf
        
    if data.data_nascimento is not None:
        paciente.data_nascimento = data.data_nascimento
    if data.telefone is not None:
        paciente.telefone = data.telefone
    if data.endereco is not None:
        paciente.endereco = data.endereco
    if data.genero is not None:
        paciente.genero = data.genero

    await db.commit()
    await db.refresh(paciente)
    await db.refresh(paciente, attribute_names=["user"])
    return paciente

@router.delete("/{paciente_id}", status_code=204)
async def delete_paciente(paciente_id: int, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(models.Paciente).where(models.Paciente.id == paciente_id))
    paciente = result.scalar_one_or_none()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    await db.delete(paciente)
    await db.commit()
