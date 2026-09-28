import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from clinicflow.backend.app.database import AsyncSessionLocal, init_db
from clinicflow.backend.app.models import User
from clinicflow.backend.app.auth import get_password_hash
from sqlalchemy import select

async def fix_admin_password():
    await init_db()
    
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.email == "admin@clinicflow.com"))
        admin = result.scalar_one_or_none()
        
        if not admin:
            print("[ERRO] Admin não encontrado")
            return
        
        # Atualizar para a senha correta do README
        admin.hashed_password = get_password_hash("admin123")
        await db.commit()
        print("[✓] Senha do admin corrigida para: admin123")

if __name__ == "__main__":
    asyncio.run(fix_admin_password())
