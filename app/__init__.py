from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

SQLALCHEMY_DATABASE_URI = "sqlite:///"

from app import rotas, modelo