import os
import re

# 1. Add PacienteUpdate to schemas.py
schemas_path = r'c:\Users\Public\ClinicFlow\clinicflow\backend\app\schemas.py'
with open(schemas_path, 'r', encoding='utf-8') as f:
    schemas_content = f.read()

if 'class PacienteUpdate' not in schemas_content:
    update_schema = """
class PacienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[date] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    genero: Optional[str] = None
"""
    schemas_content = schemas_content.replace('class PacienteOut(BaseModel):', update_schema + '\nclass PacienteOut(BaseModel):')
    with open(schemas_path, 'w', encoding='utf-8') as f:
        f.write(schemas_content)


# 2. Add PUT endpoint to pacientes.py
routers_path = r'c:\Users\Public\ClinicFlow\clinicflow\backend\app\routers\pacientes.py'
with open(routers_path, 'r', encoding='utf-8') as f:
    routers_content = f.read()

if '@router.put("/{paciente_id}"' not in routers_content:
    put_endpoint = """
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
"""
    routers_content = routers_content.replace('@router.delete("/{paciente_id}', put_endpoint + '\n@router.delete("/{paciente_id}')
    with open(routers_path, 'w', encoding='utf-8') as f:
        f.write(routers_content)


# 3. Add updatePaciente to api.js
api_js_path = r'c:\Users\Public\ClinicFlow\clinicflow\frontend\js\api.js'
with open(api_js_path, 'r', encoding='utf-8') as f:
    api_js_content = f.read()

if 'static async updatePaciente' not in api_js_content:
    api_js_content = api_js_content.replace(
        'static async createPaciente(data) { return this.request(\'/pacientes/\', { method: \'POST\', body: JSON.stringify(data) }); }',
        'static async createPaciente(data) { return this.request(\'/pacientes/\', { method: \'POST\', body: JSON.stringify(data) }); }\n    static async updatePaciente(id, data) { return this.request(`/pacientes/${id}`, { method: \'PUT\', body: JSON.stringify(data) }); }'
    )
    with open(api_js_path, 'w', encoding='utf-8') as f:
        f.write(api_js_content)


print("Backend updated.")
