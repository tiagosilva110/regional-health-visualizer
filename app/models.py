import sqlalchemy as sa
from time import time
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy.orm as so
from app import db, app, login
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask_login import UserMixin
from sqlalchemy import ForeignKey
    
class UM(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(32))
    cep: so.Mapped[str] = so.mapped_column(sa.String(8))
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Pessoa(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(32))
    birth: so.Mapped[datetime.date] = so.mapped_column(sa.Date)
    sex: so.Mapped[str] = so.mapped_column(sa.String(1))
    cep: so.Mapped[str] = so.mapped_column(sa.String(8))
    um_id: so.Mapped[int] = so.mapped_column(ForeignKey("um.id"), nullable=True)

class Consulta(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    date: so.Mapped[datetime] = so.mapped_column()
    # FK id_medico:
    # FK id_pessoa:

class Diagnostico(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # localização String
    # FK id_consulta
    # FK UM

@login.user_loader
def load_user(id):
    return db.session.get(UM, int(id))