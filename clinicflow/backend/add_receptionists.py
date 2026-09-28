import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.database import AsyncSessionLocal
from app.models import User
from app.auth import get_password_hash

async def seed_receptionists():
    async with AsyncSessionLocal() as db:
        senha_hash = get_password_hash("senha123")
        
        # Recepcionista 1
        rec1 = User(
            nome="Ana Recepcionista",
            email="ana@clinicflow.com",
            hashed_password=senha_hash,
            role="recepcionista"
        )
        # Recepcionista 2
        rec2 = User(
            nome="Carlos Recepcionista",
            email="carlos@clinicflow.com",
            hashed_password=senha_hash,
            role="recepcionista"
        )
        
        db.add(rec1)
        db.add(rec2)
        
        await db.commit()
        print("Duas recepcionistas criadas: ana@clinicflow.com e carlos@clinicflow.com com senha: senha123")

if __name__ == "__main__":
    asyncio.run(seed_receptionists())
