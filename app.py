import os
from dotenv import find_dotenv, load_dotenv
from os import environ as env

from flask import Flask, abort, redirect, render_template, request, session, url_for
from flask_login import LoginManager, login_user

from models import User, Realtor, House, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_mail import Mail, Message

app = Flask(__name__)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app.config['SECRET_KEY'] = env.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = env.get('SQLALCHEMY_DATABASE_URI')
app.config['MAIL_SERVER'] = env.get('MAIL_SERVER')
app.config['MAIL_PORT'] = env.get('MAIL_PORT')
app.config['MAIL_USE_SSL'] = env.get('MAIL_USE_SSL')
app.config['MAIL_USERNAME'] = env.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = env.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = env.get('MAIL_DEFAULT_SENDER')

db.init_app(app)
login_manager = LoginManager(app)

mail = Mail(app)
admin = Admin(app, name='Realtor', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(House, db.session))
admin.add_view(ModelView(Realtor, db.session))

@login_manager.user_loader
def get_user(id):
    return User.query.get(int(id))

@app.route('/', methods = ['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email = request.form.get('email')).first()
        if user is not None and request.form.get('password') == user.password:
            login_user(user)
            session['user_id'] = user.id
            return redirect(url_for('index'))
    else:
        return abort(status=404)

@app.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        new_user = User(
            email = request.form.get('email'),
            password = request.form.get('password')
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    
@app.route('/logout', methods = ['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/login_admin', methods = ['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        realtor = Realtor.query.filter_by(email = request.form.get('email')).first()
        if realtor is not None and request.form.get('password') == realtor.password:
            login_user(realtor)
            return "Successfully logged in"

def send_to_realtor(realtor_mail=["test@example.com"], user_email='test@example.com'):
    msg = Message(subject=f'Please contact me',
        body=f"I am interested in your house \n My email:{user_email} \n\n",
        recipients=realtor_mail,
        sender=app.config['MAIL_DEFAULT_SENDER'],
        )
    mail.send(msg)
    

@app.route('/contact_realtor/<int:id>', methods =['GET'])
def contact_realtor(id: int):
    user = User.query.filter_by(id=session.get('user_id')).first()
    realtor = Realtor.query.filter_by(id=id).first()
    send_to_realtor(realtor_mail=[realtor.email], user_email=user.email)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)