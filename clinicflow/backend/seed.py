"""
Seed assíncrono em volume: cria 30 médicos e 300 pacientes fictícios de forma otimizada.
Uso: python seed.py
"""
import asyncio
import sys
import os
import random
from datetime import date, timedelta, datetime, time
import unicodedata
from sqlalchemy import select, delete, or_
sys.path.insert(0, os.path.dirname(__file__))

from app.database import AsyncSessionLocal, init_db
from app.models import User, Medico, Paciente, Consulta
from app.auth import get_password_hash

# Listas base para geração de nomes
NOME_M = ["João", "Carlos", "José", "Roberto", "Lucas", "Pedro", "Marcos", "Rafael", "Mateus", "Felipe", "Antônio", "Paulo", "Eduardo", "Marcelo"]
NOME_F = ["Maria", "Ana", "Fernanda", "Paula", "Carla", "Juliana", "Mariana", "Patrícia", "Aline", "Camila", "Beatriz", "Letícia", "Amanda"]
SOBRENOMES = ["Silva", "Costa", "Mendes", "Lima", "Oliveira", "Souza", "Alves", "Ferreira", "Pereira", "Gomes", "Martins", "Rocha", "Ribeiro"]
ESPECIALIDADES = ["Cardiologia", "Pediatria", "Dermatologia", "Ortopedia", "Neurologia", "Oftalmologia", "Ginecologia", "Psiquiatria", "Endocrinologia"]

def gerar_nome(genero=None):
    if not genero:
        genero = random.choice(["M", "F"])
    nome = random.choice(NOME_M) if genero == "M" else random.choice(NOME_F)
    sobrenome1 = random.choice(SOBRENOMES)
    sobrenome2 = random.choice(SOBRENOMES)
    while sobrenome1 == sobrenome2:
        sobrenome2 = random.choice(SOBRENOMES)
    return f"{nome} {sobrenome1} {sobrenome2}"

def gerar_cpf():
    while True:
        cpf = [random.randint(0, 9) for _ in range(9)]
        if len(set(cpf)) > 1:
            break
            
    soma1 = sum(v * (10 - i) for i, v in enumerate(cpf))
    resto1 = soma1 % 11
    cpf.append(11 - resto1 if resto1 >= 2 else 0)
    
    soma2 = sum(v * (11 - i) for i, v in enumerate(cpf))
    resto2 = soma2 % 11
    cpf.append(11 - resto2 if resto2 >= 2 else 0)
    
    return f"{cpf[0]}{cpf[1]}{cpf[2]}.{cpf[3]}{cpf[4]}{cpf[5]}.{cpf[6]}{cpf[7]}{cpf[8]}-{cpf[9]}{cpf[10]}"

def gerar_telefone():
    return f"(11) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}"

def gerar_email(nome_completo, dominio, emails_gerados):
    # Remove prefixos
    nome = nome_completo.replace("Dr. ", "").replace("Dra. ", "").strip()
    # Remove acentos
    nome_normalizado = ''.join(c for c in unicodedata.normalize('NFD', nome) if unicodedata.category(c) != 'Mn')
    # Letras minúsculas e espaços por pontos
    base_email = nome_normalizado.lower().replace(" ", ".")
    
    email = f"{base_email}@{dominio}"
    contador = 2
    while email in emails_gerados:
        email = f"{base_email}{contador}@{dominio}"
        contador += 1
        
    emails_gerados.add(email)
    return email

async def limpar_dados_anteriores(db):
    print("[INFO] Limpando dados gerados pelo seed anterior...")
    query = select(User.id).where(User.email.like("%@seed.clinicflow.com"))
    result = await db.execute(query)
    user_ids = result.scalars().all()
    
    if user_ids:
        # Pega IDs de pacientes e médicos gerados
        pacientes_ids = (await db.execute(select(Paciente.id).where(Paciente.user_id.in_(user_ids)))).scalars().all()
        medicos_ids = (await db.execute(select(Medico.id).where(Medico.user_id.in_(user_ids)))).scalars().all()
        
        if pacientes_ids or medicos_ids:
            # Constrói o filtro or_ de forma segura
            condicoes = []
            if pacientes_ids:
                condicoes.append(Consulta.paciente_id.in_(pacientes_ids))
            if medicos_ids:
                condicoes.append(Consulta.medico_id.in_(medicos_ids))
            
            await db.execute(delete(Consulta).where(or_(*condicoes)))
            
        await db.execute(delete(Paciente).where(Paciente.user_id.in_(user_ids)))
        await db.execute(delete(Medico).where(Medico.user_id.in_(user_ids)))
        await db.execute(delete(User).where(User.id.in_(user_ids)))
        await db.flush()
        print(f"[OK] Limpeza concluída ({len(user_ids)} utilizadores de teste removidos).")

async def seed():
    await init_db()
    
    # Hash de senha pré-computado para ganho extremo de performance.
    # O hashing (bcrypt) é propositalmente lento. Fazer isso 330 vezes demoraria muito.
    print("[INFO] Gerando hash de senha base...")
    senha_hash = get_password_hash("senha123")
    
    async with AsyncSessionLocal() as db:
        try:
            # 1. Garantir a idempotência limpando dados do seed
            await limpar_dados_anteriores(db)
            
            # --- ADMIN ---
            r = await db.execute(select(User).where(User.email == "admin@clinicflow.com"))
            if not r.scalar_one_or_none():
                admin = User(nome="Administrador", email="admin@clinicflow.com",
                             hashed_password=senha_hash, role="admin")
                db.add(admin)
                await db.flush()
                print("[OK] Admin criado")
                
            # --- MÉDICOS ---
            print("[INFO] Gerando 30 Médicos em lote...")
            medicos_users = []
            emails_gerados = set()
            for i in range(1, 31):
                nome = "Dr. " + gerar_nome("M") if random.choice([True, False]) else "Dra. " + gerar_nome("F")
                email = gerar_email(nome, "seed.clinicflow.com", emails_gerados)
                
                user = User(
                    nome=nome,
                    email=email,
                    hashed_password=senha_hash,
                    role="medico"
                )
                medicos_users.append(user)
            
            db.add_all(medicos_users)
            await db.flush() # Faz o flush para obtermos os IDs gerados pelo NeonDB
            
            medicos_profiles = []
            for i, user in enumerate(medicos_users, 1):
                medico = Medico(
                    user_id=user.id,
                    crm=f"CRM/SP-{20000 + i}",
                    especialidade=random.choice(ESPECIALIDADES),
                    telefone=gerar_telefone()
                )
                medicos_profiles.append(medico)
            
            db.add_all(medicos_profiles)
            
            # --- PACIENTES ---
            print("[INFO] Gerando 300 Pacientes em lote (em chunks)...")
            
            CHUNK_SIZE = 100
            total_pacientes = 300
            
            for chunk_start in range(0, total_pacientes, CHUNK_SIZE):
                chunk_end = min(chunk_start + CHUNK_SIZE, total_pacientes)
                
                pacientes_users = []
                for i in range(chunk_start, chunk_end):
                    user = User(
                        nome=gerar_nome(),
                        email=f"paciente{i+1}@seed.clinicflow.com",
                        hashed_password=senha_hash,
                        role="paciente"
                    )
                    pacientes_users.append(user)
                    
                db.add_all(pacientes_users)
                await db.flush()
                
                pacientes_profiles = []
                for user in pacientes_users:
                    # Data de nascimento aleatória (entre 18 e 80 anos atrás)
                    dias = random.randint(18*365, 80*365)
                    data_nascimento = date.today() - timedelta(days=dias)
                    
                    paciente = Paciente(
                        user_id=user.id,
                        cpf=gerar_cpf(),
                        data_nascimento=data_nascimento,
                        telefone=gerar_telefone(),
                        endereco=f"Rua Gerada Programaticamente, {random.randint(1, 9999)} - Cidade/SP"
                    )
                    pacientes_profiles.append(paciente)
                    
                db.add_all(pacientes_profiles)
                await db.flush()
                print(f"[OK] Chunk concluído ({chunk_start} a {chunk_end}).")
                
            # --- CONSULTAS ---
            print("[INFO] Gerando Consultas em lote...")
            medicos_ids_db = (await db.execute(select(Medico.id))).scalars().all()
            pacientes_ids_db = (await db.execute(select(Paciente.id))).scalars().all()
            
            if medicos_ids_db and pacientes_ids_db:
                consultas = []
                hoje = date.today()
                
                TOTAL_CONSULTAS = 800
                
                for i in range(TOTAL_CONSULTAS):
                    medico_id = random.choice(medicos_ids_db)
                    paciente_id = random.choice(pacientes_ids_db)
                    
                    rand_crono = random.random()
                    if rand_crono < 0.2:
                        # 20% Passado (1 a 90 dias atrás)
                        delta = -random.randint(1, 90)
                        status = random.choices(["realizada", "cancelada", "nao realizada"], weights=[0.7, 0.15, 0.15])[0]
                    elif rand_crono < 0.8:
                        # 60% Presente e Próxima semana (-7 a +14 dias)
                        delta = random.randint(-7, 14)
                        if delta < 0:
                            status = random.choices(["realizada", "cancelada", "nao realizada"], weights=[0.7, 0.15, 0.15])[0]
                        elif delta == 0:
                            status = random.choices(["agendada", "realizada", "cancelada", "nao realizada"], weights=[0.4, 0.4, 0.1, 0.1])[0]
                        else:
                            status = "agendada"
                    else:
                        # 20% Futuro (15 a 60 dias)
                        delta = random.randint(15, 60)
                        status = "agendada"
                        
                    data_consulta = hoje + timedelta(days=delta)
                    
                    # Gerar horario comercial (08:00 - 17:00, em blocos de 30min)
                    hora = random.randint(8, 17)
                    minuto = random.choice([0, 30])
                    horario = time(hora, minuto)
                    
                    observacao = None
                    if status == "cancelada":
                        observacao = random.choice(["Paciente desmarcou", "Médico teve imprevisto", "Remarcada"])
                    elif status == "nao realizada":
                        observacao = random.choice(["Paciente não compareceu", "Falta sem aviso", "Atraso excedeu tolerância"])
                    elif status == "realizada" and random.random() < 0.3:
                        observacao = random.choice(["Retorno em 30 dias", "Exames solicitados", "Receita renovada"])
                        
                    consulta = Consulta(
                        medico_id=medico_id,
                        paciente_id=paciente_id,
                        data=data_consulta,
                        horario=horario,
                        status=status,
                        observacoes=observacao
                    )
                    consultas.append(consulta)
                
                # Batch insert para as consultas
                CHUNK_CONSULTAS = 200
                for c_start in range(0, TOTAL_CONSULTAS, CHUNK_CONSULTAS):
                    c_end = min(c_start + CHUNK_CONSULTAS, TOTAL_CONSULTAS)
                    db.add_all(consultas[c_start:c_end])
                    await db.flush()
                    
                print(f"[OK] {TOTAL_CONSULTAS} Consultas geradas e inseridas com sucesso.")

            await db.commit()
            print("\n[OK] Seed volumétrico concluído com sucesso!")
            
        except Exception as e:
            await db.rollback()
            print(f"\n[ERRO] Falha durante o seed: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(seed())
