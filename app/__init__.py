from flask import Flask, current_app
from flask_login import LoginManager

from app.models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'dev'
db.init_app(app)

with app.app_context():
    db.create_all()

from app import views
from app import auth

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Необходима авторизация!'
login_manager.init_app(app)

from .models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
