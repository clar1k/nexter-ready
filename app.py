import os
from dotenv import load_dotenv
from decorators import admin_required, email_confirmed
from os import environ as env
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from flask_login import LoginManager, login_required, login_user
from models import db ,User, Property, Like, Image
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from werkzeug.security import gen_salt, check_password_hash, generate_password_hash
from itsdangerous import URLSafeSerializer
from config import envConfig, Config

#! Undeployed
#TODO: Use flask flash messages.
#TODO: Sign in with Google, Facebook feature.

#? Unnecessary :D
#TODO: Change db to a PostgreSQL

app = Flask(__name__)
app.config.from_object(envConfig)

db.init_app(app)
login_manager = LoginManager(app)
mail = Mail(app)
serializer = URLSafeSerializer(app.config['SECRET_KEY'])


@login_manager.user_loader
def get_user(id):
    return User.query.get(int(id))


@app.route('/', methods = ['GET','POST'])
def index():
    properties = Property.query.all()
    property_images = Image.query.all()
    user = User.query.filter_by(id=session.get('user_id')).first()
    return render_template(
        'index.html',
        images=property_images,
        properties=properties,
        user=user
    )


@app.route('/login', methods = ['POST'])
def login():
    user = User.query.filter_by(email=request.form.get('email')).first()
    password_salt = user.salt
    password_pepper = app.config['PASSWORD_PEPPER']
    form_password = request.form.get('password') + password_salt + password_pepper
    if user and check_password_hash(user.password,form_password) and user.is_confirm:
        login_user(user)
        session['user_id'] = user.id
        return redirect('/')
    else: 
        return abort(401)


@app.route('/logout', methods = ['GET'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/register', methods = ['POST'])
def register():
    salt = gen_salt(16)
    password_pepper = app.config['PASSWORD_PEPPER']
    new_user = User(
        fullname=request.form.get('fullname'),
        email=request.form.get('email'),
        salt=salt,
        password=generate_password_hash(request.form.get('password') + salt + password_pepper)
    )
    db.session.add(new_user)
    db.session.commit()
    send_confirm_msg(new_user.email)
    login_user(new_user)
    return redirect('/')


@app.route('/confirm/<token>')
def confirm_email(token):
    email = serializer.loads(token,'email_confirm', max_age=100)
    user = User.query.filter_by(email=email).first()
    user.is_confirm = 1
    db.session.commit()
    return redirect('/')


def generate_token(email: str):
    return serializer.dumps(email,'email_confirm')


def send_confirm_msg(email: str) -> None:
    token = generate_token(email)
    msg = Message(
        subject="Confirm your email",
        html=f'Press the <a href="http://127.0.0.1:5000/confirm/{token}"target="_blank"> link </a> to confirm your email' ,
        recipients=[email],
        sender=('Nexter Ready',app.config['MAIL_DEFAULT_SENDER']),
    )
    mail.send(msg)


def send_to_realtor(realtor_mail=["test@example.com"], user_email='test@example.com'):
    msg = Message(subject=f'Please contact me',
        body=f"I am interested in your property \n My email: {user_email} \n\n",
        recipients=realtor_mail,
        sender=('Nexter Ready',app.config['MAIL_DEFAULT_SENDER']),
        )
    mail.send(msg)


@app.route('/contact_realtor/<int:id>', methods =['GET'])
@login_required
def contact_realtor(id: int):
        user = User.query.filter_by(id=session.get('user_id')).first()
        realtor = User.query.filter_by(id=id).first()
        send_to_realtor(realtor_mail=[realtor.email], user_email=user.email)
        return redirect('/')


@app.route('/add-property', methods=['GET'])
@login_required
@admin_required
def add_property():
    return render_template('newProperty.html') 


def add_filename(filename: str, property_id: int):
        new_image = Image(property_id=property_id,image_filename=filename)
        db.session.add(new_image)
        db.session.commit()


def save_images(images: list, property_id: int): 
    for image in images:
        filename = secure_filename(image.filename)
        add_filename(image.filename, property_id)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


@app.route('/add',methods=['POST'])
@admin_required
def add_prop():
    if request.form.get('action') == 'submit':
        new_property = Property(
            name=request.form.get('name'),
            author_id=session.get('user_id'),
            rooms=request.form.get('rooms'),
            location=request.form.get('location'),
            price=request.form.get('price'),
            house_square=request.form.get('area'),
        )
        db.session.add(new_property)
        db.session.commit()
        _property = Property.query.filter_by(name=request.form.get('name')).first()
        images = request.files.getlist("images")
        if images:
            save_images(images,_property.id)
        return redirect('/')
    else:
        return '', 204


@app.route('/property/<int:id>')
def property(id: int):
    property = Property.query.filter_by(id=id).first()
    images = Image.query.filter_by(property_id=id)
    return render_template(
        'viewProperty.html', 
        property=property,
        images=images,
        logged_in=session.get('user_id')
    )


@app.route('/add-to-favorites/<int:id>', methods=['GET'])
def add_to_favorites(id: int):
    favorite = Like.query.filter_by(user_id=session.get('user_id'), favorite_property=id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()        
        return '', 204
    else:
        favorite = Like(user_id=session.get('user_id'), favorite_property=id)
        db.session.add(favorite)
        db.session.commit()
        return '', 204


def create_db():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    app.run(debug=True)