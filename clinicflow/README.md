# ClinicFlow

Sistema acadêmico completo para gestão de clínicas médicas, construído com Python, FastAPI, SQLAlchemy e PostgreSQL.

## Funcionalidades

- **REST API** (FastAPI) com JWT Authentication e Role-Based Access Control.
- **Frontend Customizado** utilizando HTML/CSS/JS puros, interagindo com as APIs.
- **Testes** integrados (pytest).
- Documentação automática OpenAPI (Swagger/ReDoc).

## Como Executar Localmente

### 1. Requisitos
- Python 3.10+
- Banco de Dados PostgreSQL (Local ou Nuvem)

### 2. Configurar o Backend
No diretório `backend`:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Crie o arquivo `.env` (baseado no `.env.example` caso exista) com sua string de conexão com o banco de dados, por exemplo:
```env
DATABASE_URL=postgresql://user:password@host/dbname
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3. Rodar Seeds (Opcional)
As tabelas do banco de dados são criadas automaticamente ao iniciar o servidor. Para popular o banco com dados iniciais:
```bash
python seed.py
```

### 4. Iniciar o Servidor
```bash
uvicorn app.main:app --reload --port 8000
```
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 5. Frontend
Você pode abrir o arquivo `index.html` ou usar uma extensão como Live Server ou `python -m http.server 8080` no diretório `frontend`.

Acesse `http://localhost:8080` e faça login com os usuários de teste.

## Usuários de Demonstração (Seed)

- **Admin:** ``admin@clinicflow.com / `admin123`
- **Médico:** `medico@clinicflow.com` / `medico123`
- **Paciente:** `paciente@clinicflow.com` / `paciente123`

*(As senhas acima são apenas para fins de teste no ambiente de desenvolvimento)*
