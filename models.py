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
    is_admin = db.Column(db.Boolean(), default=0)
class House(db.Model):
    __tablename__ = 'Properties'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('Users.id'))
    name = db.Column(db.String(19), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    house_square = db.Column(db.Float())
    rooms = db.Column(db.String(300))
    price = db.Column(db.Float())
    image_filename = db.Column(db.String(255), nullable = False)

class Favorites(db.Model):
    __tablename__= 'Favorites'
    user_id = db.Column('user_id',db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    favorite_subject = db.Column(db.Integer, db.ForeignKey('Properties.id'))