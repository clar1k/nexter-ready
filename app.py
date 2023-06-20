import os
from dotenv import load_dotenv
from os import environ as env
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from flask_login import LoginManager, login_required, login_user
from models import User, Property, db, Favorites, Image
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

app = Flask(__name__)

load_dotenv('.env')
app.config['SECRET_KEY'] = env.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = env.get('SQLALCHEMY_DATABASE_URI')
app.config['MAIL_SERVER'] = env.get('MAIL_SERVER')
app.config['MAIL_PORT'] = env.get('MAIL_PORT')
app.config['MAIL_USE_SSL'] = env.get('MAIL_USE_SSL')
app.config['MAIL_USERNAME'] = env.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = env.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = env.get('MAIL_DEFAULT_SENDER')
app.config['UPLOAD_FOLDER'] = env.get('UPLOAD_FOLDER') 

db.init_app(app)
login_manager = LoginManager(app)
mail = Mail(app)


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
    if request.method == 'POST':
        try:
            user = User.query.filter_by(email=request.form.get('email')).first()
            if user is not None and request.form.get('password') == user.password:
                login_user(user)
                session['user_id'] = user.id
                return redirect('/')
        except Exception as e:
            return str(e)
    else:
        return abort(status=404)


@app.route('/logout', methods = ['GET'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        new_user = User(
            fullname=request.form.get('fullname'),
            email=request.form.get('email'),
            password = request.form.get('password')
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')



def send_to_realtor(realtor_mail=["test@example.com"], user_email='test@example.com'):
    msg = Message(subject=f'Please contact me',
        body=f"I am interested in your property \n My email: {user_email} \n\n",
        recipients=realtor_mail,
        sender=app.config['MAIL_DEFAULT_SENDER'],
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
def add_property():
    user = User.query.get(session.get('user_id'))
    if not user.is_admin:
        return abort(403)
    return render_template('newProperty.html') 


def add_filename(filename: str, property_id: int):
        new_image = Image(property_id=property_id,image_filename=filename)
        db.session.add(new_image)
        db.session.commit()


def save_images(images , property_id: int): 
    for image in images:
        filename = secure_filename(image.filename)
        add_filename(image.filename, property_id)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


@app.route('/add',methods=['POST'])
def add_prop():
    if request.form.get('action') == 'submit':
        new_property = Property(
            name=request.form.get('name'),
            user_id=session.get('user_id'),
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
    favorite = Favorites(user_id=session.get('user_id'),favorite_subject=id)
    is_already_favorite = Favorites.query.filter_by(user_id=session.get('user_id'),favorite_subject=id).first()
    if is_already_favorite:
        return redirect('/')
    db.session.add(favorite)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)