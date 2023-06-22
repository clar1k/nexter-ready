from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Numeric, UniqueConstraint

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    fullname = db.Column(db.String(30), nullable=True, unique=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    is_admin = db.Column(db.Boolean(), default=0)
class Property(db.Model):
    __tablename__ = 'Properties'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('Users.id'))
    name = db.Column(db.String(19), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    house_square = db.Column(db.Float(), nullable=False)
    rooms = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Float(), nullable=False)
class Favorites(db.Model):
    __tablename__= 'Favorites'
    user_id = db.Column('user_id',db.Integer, db.ForeignKey('Users.id'), unique=False, primary_key=True)
    favorite_property = db.Column(db.Integer, db.ForeignKey('Properties.id'), primary_key=True)
    __table_args__ = (
        UniqueConstraint('user_id', 'favorite_property', name='uq_user_property'),
    )
class Image(db.Model):
    __tablename__='PropertyImages'
    property_id = db.Column(db.Integer, unique=False, primary_key=True)
    image_filename = db.Column(db.String(255), unique=False, primary_key=True)
    __table_args__ = (
        UniqueConstraint('property_id', 'image_filename', name='uq_property_image'),
    )