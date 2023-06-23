from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Numeric
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
db = SQLAlchemy()
class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    fullname = db.Column(db.String(30))
    password = db.Column(db.String(255))
    salt = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    is_confirm = db.Column(db.Boolean(), default=0)
    is_admin = db.Column(db.Boolean(), default=0)

class Property(db.Model):
    __tablename__ = 'Properties'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    name = db.Column(db.String(19), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    house_square = db.Column(db.Float(), nullable=False)
    rooms = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Float(), nullable=False)

class Like(db.Model):
    __tablename__= 'Likes'
    user_id = db.Column('user_id',db.Integer, db.ForeignKey('Users.id'),primary_key=True)
    favorite_property = db.Column(db.Integer, db.ForeignKey('Properties.id'),primary_key=True)

class Image(db.Model):
    __tablename__='Images'
    property_id = db.Column(db.Integer, unique=False, primary_key=True)
    image_filename = db.Column(db.String(255), unique=False, primary_key=True)