from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, time, datetime


# ─── Auth ───────────────────────────────────────────────────
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    nome: str


# ─── User ───────────────────────────────────────────────────
class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    password: str
    role: str = "paciente"


class UserOut(BaseModel):
    id: int
    nome: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class UserList(BaseModel):
    items: list[UserOut]
    total: int


# ─── Médico ─────────────────────────────────────────────────
class MedicoCreate(BaseModel):
    nome: str
    email: EmailStr
    password: str
    crm: str
    especialidade: str
    telefone: Optional[str] = None


class MedicoOut(BaseModel):
    id: int
    crm: str
    especialidade: str
    telefone: Optional[str]
    user: UserOut

    class Config:
        from_attributes = True


# ─── Paciente ───────────────────────────────────────────────
class PacienteCreate(BaseModel):
    nome: str
    email: EmailStr
    password: str
    cpf: str
    data_nascimento: Optional[date] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None


class PacienteOut(BaseModel):
    id: int
    cpf: str
    data_nascimento: Optional[date]
    telefone: Optional[str]
    endereco: Optional[str]
    user: UserOut

    class Config:
        from_attributes = True


# ─── Consulta ───────────────────────────────────────────────
class ConsultaCreate(BaseModel):
    medico_id: int
    paciente_id: int
    data: date
    horario: time
    observacoes: Optional[str] = None


class ConsultaUpdate(BaseModel):
    status: Optional[str] = None
    observacoes: Optional[str] = None
    data: Optional[date] = None
    horario: Optional[time] = None


class ConsultaOut(BaseModel):
    id: int
    data: date
    horario: time
    status: str
    observacoes: Optional[str]
    medico: MedicoOut
    paciente: PacienteOut

    class Config:
        from_attributes = True

class ConsultaList(BaseModel):
    items: list[ConsultaOut]
    total: int

class MedicoList(BaseModel):
    items: list[MedicoOut]
    total: int

class PacienteList(BaseModel):
    items: list[PacienteOut]
    total: int
