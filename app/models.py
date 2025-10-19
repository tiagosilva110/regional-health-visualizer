import sqlalchemy as sa
from time import time
from datetime import datetime, date
from typing import Optional
import sqlalchemy.orm as so
from app import db, app, login
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask_login import UserMixin
from sqlalchemy import ForeignKey
    
class UM(UserMixin, db.Model):
    __tablename__ = 'um'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(32))
    cep: so.Mapped[str] = so.mapped_column(sa.String(8))
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Medico(db.Model):
    __tablename__ = 'medico'
    crm: so.Mapped[str] = so.mapped_column(sa.String(16), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(32))
    um_id: so.Mapped[int] = so.mapped_column(ForeignKey("um.id"), nullable=True)

class Pessoa(db.Model):
    __tablename__ = 'pessoa'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(32))
    birth: so.Mapped[datetime.date] = so.mapped_column(sa.Date)
    sex: so.Mapped[str] = so.mapped_column(sa.String(1))
    cep: so.Mapped[str] = so.mapped_column(sa.String(8))
    um_id: so.Mapped[int] = so.mapped_column(ForeignKey("um.id"), nullable=True)

class Doenca(db.Model):
    __tablename__ = 'doenca'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    tipo: so.Mapped[str] = so.mapped_column(sa.String(32))

    def getById(id):
        return None

class Diagnostico(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date)
    medico_crm: so.Mapped[int] = so.mapped_column(ForeignKey("medico.crm"), nullable=True)
    pessoa_id: so.Mapped[int] = so.mapped_column(ForeignKey("pessoa.id"), nullable=True)
    coord: so.Mapped[str] = so.mapped_column(sa.String(32))
    id_doenca: so.Mapped[int] = so.mapped_column(ForeignKey("doenca.id"),nullable=True)

@login.user_loader
def load_user(id):
    return db.session.get(UM, int(id))