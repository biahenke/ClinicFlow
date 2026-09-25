from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Date, Time
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="paciente")  # admin, medico, paciente, receptionist
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    medico = relationship("Medico", back_populates="user", uselist=False, lazy="selectin")
    paciente = relationship("Paciente", back_populates="user", uselist=False, lazy="selectin")


class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    crm = Column(String(20), unique=True, nullable=False)
    especialidade = Column(String(100), nullable=False)
    telefone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="medico", lazy="selectin")
    consultas = relationship("Consulta", back_populates="medico")


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    data_nascimento = Column(Date)
    telefone = Column(String(20))
    endereco = Column(Text)
    genero = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="paciente", lazy="selectin")
    consultas = relationship("Consulta", back_populates="paciente")


class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, index=True)
    medico_id = Column(Integer, ForeignKey("medicos.id"), nullable=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=True)
    data = Column(Date, nullable=False)
    horario = Column(Time, nullable=False)
    status = Column(String(20), default="agendada")  # agendada, realizada, cancelada
    observacoes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    medico = relationship("Medico", back_populates="consultas", lazy="selectin")
    paciente = relationship("Paciente", back_populates="consultas", lazy="selectin")
