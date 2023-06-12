from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Numeric

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    is_confirm = db.Column(db.Boolean(), default = 0)

class Realtor(db.Model, UserMixin):
    __tablename__ = 'Realtors'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean(), default = 1)

class House(db.Model):
    __tablename__ = 'Houses'
    id = db.Column(db.Integer(), primary_key = True)
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=True)
    construction_year = db.Column(db.Integer(), default = 0)
    location = db.Column(db.String(255), default = "")
    house_square = db.Column(db.Numeric())
    furniture_filling = db.Column(db.String(300))
    price = db.Column(db.Numeric(12,2))