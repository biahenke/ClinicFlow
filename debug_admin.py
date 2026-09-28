import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from clinicflow.backend.app.database import AsyncSessionLocal, init_db
from clinicflow.backend.app.models import User
from clinicflow.backend.app.auth import get_password_hash, verify_password
from sqlalchemy import select

async def debug_admin():
    await init_db()
    
    async with AsyncSessionLocal() as db:
        # Recuperar admin
        result = await db.execute(select(User).where(User.email == "admin@clinicflow.com"))
        admin = result.scalar_one_or_none()
        
        if not admin:
            print("[ERRO] Admin não encontrado")
            return
        
        print(f"[INFO] Admin encontrado:")
        print(f"  - ID: {admin.id}")
        print(f"  - Email: {admin.email}")
        print(f"  - Nome: {admin.nome}")
        print(f"  - Role: {admin.role}")
        print(f"  - is_active: {admin.is_active}")
        print(f"  - Hashed password (primeiros 50 chars): {admin.hashed_password[:50]}...")
        
        # Testar verificação de senha
        password_to_test = "senha123"
        is_valid = verify_password(password_to_test, admin.hashed_password)
        print(f"\n[DEBUG] Verificação de senha '{password_to_test}': {is_valid}")
        
        # Gerar novo hash e comparar
        print(f"\n[DEBUG] Gerando novo hash para 'senha123'...")
        new_hash = get_password_hash("senha123")
        print(f"  - Novo hash: {new_hash[:50]}...")
        new_is_valid = verify_password("senha123", new_hash)
        print(f"  - Verificação do novo hash: {new_is_valid}")

if __name__ == "__main__":
    asyncio.run(debug_admin())
