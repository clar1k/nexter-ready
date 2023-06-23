from os import environ as env
from dotenv import load_dotenv
load_dotenv('.env')
class Config:
    SECRET_KEY = env.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI=env.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS=env.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY=env.get('SECRET_KEY')
    MAIL_SERVER=env.get('MAIL_SERVER')
    MAIL_PORT=env.get('MAIL_PORT')
    MAIL_USE_SSL=env.get('MAIL_USE_SSL')
    MAIL_USERNAME=env.get('MAIL_USERNAME')
    MAIL_PASSWORD=env.get('MAIL_PASSWORD')
    PASSWORD_PEPPER=env.get('PASSWORD_PEPPER')
    MAIL_DEFAULT_SENDER=env.get('MAIL_DEFAULT_SENDER')
    UPLOAD_FOLDER=env.get('UPLOAD_FOLDER')