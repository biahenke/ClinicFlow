import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from clinicflow.backend.app.database import AsyncSessionLocal, init_db
from clinicflow.backend.app.models import User
from clinicflow.backend.app.auth import get_password_hash
from sqlalchemy import select

async def create_admin():
    await init_db()
    
    async with AsyncSessionLocal() as db:
        # Verificar se admin já existe
        result = await db.execute(select(User).where(User.email == "admin@clinicflow.com"))
        existing = result.scalar_one_or_none()
        
        if existing:
            print(f"[INFO] Admin já existe: {existing.email}")
            return
        
        # Criar novo admin
        senha_hash = get_password_hash("senha123")
        admin = User(
            nome="Administrador",
            email="admin@clinicflow.com",
            hashed_password=senha_hash,
            role="admin"
        )
        db.add(admin)
        await db.commit()
        print(f"[OK] Admin criado com sucesso: admin@clinicflow.com")

if __name__ == "__main__":
    asyncio.run(create_admin())
