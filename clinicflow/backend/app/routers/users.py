from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, update
from app.database import get_db
from app import models, schemas
from app.auth import get_password_hash
from app.dependencies import require_admin
from typing import Optional
from pydantic import BaseModel

class UserCreateFull(schemas.UserCreate):
    # Medico fields
    crm: Optional[str] = None
    especialidade: Optional[str] = None
    telefone: Optional[str] = None
    # Paciente fields
    cpf: Optional[str] = None
    data_nascimento: Optional[str] = None # Using str to simplify parsing or date
    endereco: Optional[str] = None

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=schemas.UserList)
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    role: Optional[str] = None,
    current_user: models.User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    query = select(models.User)
    if role:
        query = query.where(models.User.role == role)
    
    # Count total
    total_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(total_query)
    total = total_result.scalar() or 0
    
    # Get items
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    
    return {"items": items, "total": total}

@router.post("/", response_model=schemas.UserOut)
async def create_user(
    data: UserCreateFull,
    current_user: models.User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    # Check if email exists
    result = await db.execute(select(models.User).where(models.User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
        
    hashed_password = get_password_hash(data.password)
    new_user = models.User(
        nome=data.nome,
        email=data.email,
        hashed_password=hashed_password,
        role=data.role,
        is_active=True
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    if data.role == "medico" and data.crm and data.especialidade:
        new_medico = models.Medico(
            user_id=new_user.id,
            crm=data.crm,
            especialidade=data.especialidade,
            telefone=data.telefone
        )
        db.add(new_medico)
        await db.commit()
    elif data.role == "paciente" and data.cpf:
        new_paciente = models.Paciente(
            user_id=new_user.id,
            cpf=data.cpf,
            telefone=data.telefone,
            endereco=data.endereco
        )
        if data.data_nascimento:
            from datetime import datetime
            try:
                new_paciente.data_nascimento = datetime.strptime(data.data_nascimento, "%Y-%m-%d").date()
            except ValueError:
                pass
        db.add(new_paciente)
        await db.commit()
        
    return new_user

@router.put("/{user_id}", response_model=schemas.UserOut)
async def update_user(
    user_id: int,
    data: schemas.UserUpdate,
    current_user: models.User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
    if data.email and data.email != user.email:
        email_check = await db.execute(select(models.User).where(models.User.email == data.email))
        if email_check.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email já cadastrado")
            
    if data.nome is not None:
        user.nome = data.nome
    if data.email is not None:
        user.email = data.email
    if data.role is not None:
        user.role = data.role
    if data.is_active is not None:
        user.is_active = data.is_active
    if data.password is not None:
        user.hashed_password = get_password_hash(data.password)
        
    await db.commit()
    await db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: models.User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
    # Delete Medico/Paciente profile if exists, leaving consultas orphaned
    if user.role == "medico":
        med_res = await db.execute(select(models.Medico).where(models.Medico.user_id == user_id))
        medico = med_res.scalar_one_or_none()
        if medico:
            await db.execute(update(models.Consulta).where(models.Consulta.medico_id == medico.id).values(medico_id=None))
            await db.delete(medico)
            
    elif user.role == "paciente":
        pac_res = await db.execute(select(models.Paciente).where(models.Paciente.user_id == user_id))
        paciente = pac_res.scalar_one_or_none()
        if paciente:
            await db.execute(update(models.Consulta).where(models.Consulta.paciente_id == paciente.id).values(paciente_id=None))
            await db.delete(paciente)

    await db.delete(user)
    await db.commit()
    return None
