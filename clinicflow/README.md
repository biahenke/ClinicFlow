# ClinicFlow

Sistema acadêmico completo para gestão de clínicas médicas, construído com Python, FastAPI, SQLAlchemy e PostgreSQL.

## Funcionalidades

- **REST API** (FastAPI) com JWT Authentication e Role-Based Access Control.
- **SOAP Service** (Spyne) funcional exposto no endpoint `/soap`.
- **Frontend Customizado** utilizando HTML/CSS/JS puros, interagindo com as APIs.
- **Testes** integrados (pytest).
- **Docker Compose** para o banco de dados PostgreSQL.
- Documentação automática OpenAPI (Swagger/ReDoc).

## Como Executar Localmente

### 1. Requisitos
- Docker e Docker Compose
- Python 3.10+

### 2. Iniciar o Banco de Dados
```bash
docker-compose up -d
```

### 3. Configurar o Backend
No diretório `backend`:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Crie o `.env` (exemplo fornecido em `.env.example`).

### 4. Rodar Migrations e Seeds
```bash
alembic upgrade head
python seed.py
```

### 5. Iniciar o Servidor (REST e SOAP)
```bash
uvicorn app.main:app --reload --port 8000
```
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- SOAP WSDL: `http://localhost:8000/soap?wsdl`

### 6. Frontend
Você pode abrir o arquivo `index.html` ou usar uma extensão como Live Server ou `python -m http.server 8080` no diretório `frontend`.

Acesse `http://localhost:8080` e faça login com os usuários de teste.

## Usuários de Demonstração (Seed)

- **Admin:** `admin@clinicflow.com` / `admin123`
- **Médico:** `medico@clinicflow.com` / `medico123`
- **Paciente:** `paciente@clinicflow.com` / `paciente123`

*(As senhas acima são apenas para fins de teste no ambiente de desenvolvimento)*
