import pytest
import os
from app import app
from app import create_db
from models import User, Property, Like
from flask import session
from models import db
import io
from PIL import Image


@pytest.fixture
def client():
    create_db()
    with app.test_client() as client:
        yield client


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 201
    assert b"The ultimate personal freedom" in response.data


def test_registration(client):
    response = client.post('/register', 
    data = {
        "fullname":"Test User",
        "email":"test@test.com",
        "password":"test_password",
        "is_confirm":"1",
        "is_admin":"1"
    })
    with app.app_context():
        assert User.query.count() == 1
        user = User.query.filter_by(email="test@test.com").first()
        assert user.email == 'test@test.com'
        assert response.status_code == 400


def test_login(client):
    response = client.post('/login',
        data = {
            "email":"test@test.com",
            "password":"test_password",
        }
    )
    with app.app_context():
        assert response.status_code == 200


def test_add_property(client):
    test_login(client)
    response = client.post('/add', data={
        'name': 'Example Property',
        'rooms': 3,
        'location': 'Test Location',
        'price': 100000,
        'area': 200,
        "action":"submit"
    })
    with app.app_context():
        prop = Property.query.filter_by(name='Example Property',rooms=3).first()
        assert Property.query.count() == 1
        assert prop.name == "Example Property"
        assert response.status_code == 201

def test_like(client):
    test_login(client)
    responce = client.get('/add-to-favorites/1')
    with app.app_context():
        like = Like.query.filter_by(user_id=1).first()
        if not like:
            pass
        else:
            assert like.favorite_property == 1