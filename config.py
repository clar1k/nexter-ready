from os import environ as env
from dotenv import load_dotenv
load_dotenv('.env')
class envConfig:
    SECRET_KEY=env.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI=env.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER=env.get('MAIL_SERVER')
    MAIL_PORT=env.get('MAIL_PORT')
    MAIL_USE_SSL=env.get('MAIL_USE_SSL')
    MAIL_USERNAME=env.get('MAIL_USERNAME')
    MAIL_PASSWORD=env.get('MAIL_PASSWORD')
    PASSWORD_PEPPER=env.get('PASSWORD_PEPPER')
    MAIL_DEFAULT_SENDER=env.get('MAIL_DEFAULT_SENDER')
    UPLOAD_FOLDER=env.get('UPLOAD_FOLDER')


class Config:
    SECRET_KEY="EHFNAISOJF@!*Y*(G*@!(EG*(@EY)))"
    SQLALCHEMY_DATABASE_URI="sqlite:///realtor.db"
    PASSWORD_PEPPER="a912j30mv0912he"
    UPLOAD_FOLDER="static/uploads"