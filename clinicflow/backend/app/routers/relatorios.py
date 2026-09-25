from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date, timedelta
from app.database import get_db
from app import models
from app.dependencies import get_current_user

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

@router.get("/summary")
async def get_summary(
    start_date: date | None = None,
    end_date: date | None = None,
    db: AsyncSession = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role == 'paciente':
        raise HTTPException(status_code=403, detail="Acesso negado")
        
    query = select(models.Consulta)
    
    if start_date:
        query = query.where(models.Consulta.data >= start_date)
    if end_date:
        query = query.where(models.Consulta.data <= end_date)
    
    if current_user.role == 'medico':
        result = await db.execute(select(models.Medico).where(models.Medico.user_id == current_user.id))
        medico_profile = result.scalar_one_or_none()
        if medico_profile:
            query = query.where(models.Consulta.medico_id == medico_profile.id)
        else:
            return {"items": []}

    result = await db.execute(query)
    consultas = result.scalars().all()
    
    hoje = date.today()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)
    
    metrics = {
        "periodo": {
            "passado": 0,
            "semana_atual": 0,
            "futuro": 0
        },
        "status": {
            "agendada": 0,
            "realizada": 0,
            "cancelada": 0,
            "nao_realizada": 0
        },
        "volume_medico": {},
        "volume_especialidade": {}
    }
    
    for c in consultas:
        if c.data < inicio_semana:
            metrics["periodo"]["passado"] += 1
        elif inicio_semana <= c.data <= fim_semana:
            metrics["periodo"]["semana_atual"] += 1
        else:
            metrics["periodo"]["futuro"] += 1
            
        status_key = c.status.lower().replace(" ", "_")
        if status_key in metrics["status"]:
            metrics["status"][status_key] += 1
            
        if current_user.role != 'medico':
            if c.medico:
                nome_medico = c.medico.user.nome if c.medico.user else f"Médico {c.medico_id}"
                esp = c.medico.especialidade
                metrics["volume_medico"][nome_medico] = metrics["volume_medico"].get(nome_medico, 0) + 1
                metrics["volume_especialidade"][esp] = metrics["volume_especialidade"].get(esp, 0) + 1
                
    return metrics
