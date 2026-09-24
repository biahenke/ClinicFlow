from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import date, timedelta
from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(prefix="/consultas", tags=["Consultas"])


@router.get("/", response_model=schemas.ConsultaList)
async def list_consultas(
    skip: int = 0, 
    limit: int = 100, 
    data: Optional[date] = None,
    medico: Optional[str] = None,
    paciente: Optional[str] = None,
    especialidade: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    query = select(models.Consulta).join(models.Medico, models.Consulta.medico_id == models.Medico.id)\
                                   .join(models.Paciente, models.Consulta.paciente_id == models.Paciente.id)\
                                   .join(models.User, models.Medico.user_id == models.User.id, isouter=True) # alias conflict if joining User twice? let's do it simpler.

    query = select(models.Consulta)
    
    # RBAC rules
    if current_user.role == 'medico':
        # Retrieve the Medico profile for this user
        result = await db.execute(select(models.Medico).where(models.Medico.user_id == current_user.id))
        medico_profile = result.scalar_one_or_none()
        if medico_profile:
            query = query.where(models.Consulta.medico_id == medico_profile.id)
        else:
            # If for some reason medico profile doesn't exist, return empty
            return {"items": [], "total": 0}
            
    elif current_user.role == 'paciente':
        # Similarly for patients
        result = await db.execute(select(models.Paciente).where(models.Paciente.user_id == current_user.id))
        paciente_profile = result.scalar_one_or_none()
        if paciente_profile:
            query = query.where(models.Consulta.paciente_id == paciente_profile.id)
        else:
            return {"items": [], "total": 0}

    if data:
        query = query.where(models.Consulta.data == data)
        
    if status:
        query = query.where(models.Consulta.status.ilike(f"%{status}%"))

    # We can join Medico/Paciente to filter by names or especialidade if needed by admin
    if current_user.role in ['admin', 'receptionist']:
        # just basic filtering if passed directly (e.g. if medico is an ID)
        if medico and medico.isdigit():
            query = query.where(models.Consulta.medico_id == int(medico))
        elif medico: # rudimentary text search on Medico relation not implemented yet, just ignoring for now or could implement
            query = query.join(models.Medico).join(models.User, models.Medico.user_id == models.User.id).where(models.User.nome.ilike(f"%{medico}%"))
            
        if paciente and paciente.isdigit():
            query = query.where(models.Consulta.paciente_id == int(paciente))
            
        if especialidade:
            query = query.join(models.Medico, models.Consulta.medico_id == models.Medico.id).where(models.Medico.especialidade.ilike(f"%{especialidade}%"))
            

    query = query.order_by(models.Consulta.data.asc(), models.Consulta.horario.asc())
    
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    
    return {"items": items, "total": total or 0}


@router.get("/estatisticas/semana")
async def estatisticas_semana(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    # Retornar contagem de consultas de Seg a Sex desta semana
    hoje = date.today()
    # Segunda-feira da semana atual
    segunda = hoje - timedelta(days=hoje.weekday())
    
    # Array de 5 dias (Seg a Sex)
    dados = []
    for i in range(5):
        dia_alvo = segunda + timedelta(days=i)
        query = select(func.count(models.Consulta.id)).where(
            models.Consulta.data == dia_alvo,
            models.Consulta.status.notin_(["cancelada", "canceladas", "nao realizada", "falta"])
        )
        result = await db.execute(query)
        total = result.scalar_one()
        dados.append(total)
        
    return {"dados_semana": dados}


@router.get("/estatisticas/status")
async def estatisticas_status(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    hoje = date.today()
    segunda = hoje - timedelta(days=hoje.weekday())
    domingo = segunda + timedelta(days=6)

    query = select(models.Consulta.status, func.count(models.Consulta.id))\
        .where(models.Consulta.data >= segunda, models.Consulta.data <= domingo)\
        .group_by(models.Consulta.status)
    
    result = await db.execute(query)
    contagens = result.all()
    
    total = sum(count for _, count in contagens)
    
    status_dict = {
        "realizadas": 0,
        "agendadas": 0,
        "canceladas": 0,
        "nao_realizadas": 0
    }
    
    for status, count in contagens:
        if status == "realizada":
            status_dict["realizadas"] += count
        elif status == "agendadas" or status == "agendada":
            status_dict["agendadas"] += count
        elif status in ["canceladas", "cancelada"]:
            status_dict["canceladas"] += count
        elif status in ["nao realizada", "falta"]:
            status_dict["nao_realizadas"] += count

    if total > 0:
        return {
            "realizadas": round((status_dict["realizadas"] / total) * 100),
            "agendadas": round((status_dict["agendadas"] / total) * 100),
            "canceladas": round((status_dict["canceladas"] / total) * 100),
            "nao_realizadas": round((status_dict["nao_realizadas"] / total) * 100)
        }
    return {"realizadas": 0, "agendadas": 0, "canceladas": 0, "nao_realizadas": 0}


@router.get("/{consulta_id}", response_model=schemas.ConsultaOut)
async def get_consulta(consulta_id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(models.Consulta).where(models.Consulta.id == consulta_id))
    consulta = result.scalar_one_or_none()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return consulta


@router.post("/", response_model=schemas.ConsultaOut, status_code=201)
async def create_consulta(data: schemas.ConsultaCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    r_medico = await db.execute(select(models.Medico).where(models.Medico.id == data.medico_id))
    medico = r_medico.scalar_one_or_none()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    r_paciente = await db.execute(select(models.Paciente).where(models.Paciente.id == data.paciente_id))
    paciente = r_paciente.scalar_one_or_none()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    if medico.especialidade and "ginecologia" in medico.especialidade.lower():
        if paciente.genero and paciente.genero.lower() in ["m", "male", "masculino"]:
            raise HTTPException(status_code=400, detail="Consultas de Ginecologia não são permitidas para pacientes do sexo masculino")

    consulta = models.Consulta(
        medico_id=data.medico_id,
        paciente_id=data.paciente_id,
        data=data.data,
        horario=data.horario,
        observacoes=data.observacoes
    )
    db.add(consulta)
    await db.commit()
    await db.refresh(consulta)
    return consulta


@router.patch("/{consulta_id}", response_model=schemas.ConsultaOut)
async def update_consulta(consulta_id: int, data: schemas.ConsultaUpdate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(models.Consulta).where(models.Consulta.id == consulta_id))
    consulta = result.scalar_one_or_none()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(consulta, field, value)

    await db.commit()
    await db.refresh(consulta)
    return consulta


@router.patch("/{consulta_id}/status", response_model=schemas.ConsultaOut)
async def update_consulta_status(consulta_id: int, data: schemas.ConsultaStatusUpdate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    valid_statuses = ['agendada', 'cancelada', 'nao realizada', 'realizada']
    if data.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Status inválido")

    result = await db.execute(select(models.Consulta).where(models.Consulta.id == consulta_id))
    consulta = result.scalar_one_or_none()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    # RBAC validation
    if current_user.role == 'medico' or current_user.role == 'doctor':
        result_medico = await db.execute(select(models.Medico).where(models.Medico.user_id == current_user.id))
        medico_profile = result_medico.scalar_one_or_none()
        if not medico_profile or consulta.medico_id != medico_profile.id:
            raise HTTPException(status_code=403, detail="Acesso negado. Você só pode alterar suas próprias consultas.")
    elif current_user.role not in ['admin', 'receptionist']:
        raise HTTPException(status_code=403, detail="Acesso negado. Você não tem permissão para alterar o status.")

    consulta.status = data.status
    await db.commit()
    await db.refresh(consulta)
    return consulta


@router.delete("/{consulta_id}", status_code=204)
async def delete_consulta(consulta_id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(models.Consulta).where(models.Consulta.id == consulta_id))
    consulta = result.scalar_one_or_none()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    await db.delete(consulta)
    await db.commit()
