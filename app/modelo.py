import sqlalchemy as sa
from time import time
from datetime import datetime, timezone
import sqlalchemy.orm as so
from app import db


    
class UM(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(32))
    cep: so.Mapped[int] = so.mapped_column()

class Medico(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(32))
    # FK UM

class Pessoa(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(32))
    data_nasc: so.Mapped[datetime] = so.mapped_column()
    cep: so.Mapped[int] = so.mapped_column()

class Consulta(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    data_hora: so.Mapped[datetime] = so.mapped_column()
    # FK id_medico:
    # FK id_pessoa:

class Diagnostico(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # FK id_consulta
    # FK UM