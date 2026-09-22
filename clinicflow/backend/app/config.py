from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://clinicflow_user:clinicflow_password@localhost:5432/clinicflow_db")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey_clinicflow_2024")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
