from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .auth import auth_app
from .tasks import tasks_app

app = Flask(__name__)
app.register_blueprint(auth_app)
app.register_blueprint(tasks_app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'dev'
db = SQLAlchemy()
db.init_app(app)

from .auth.models import User
from .tasks.models import Task

with app.app_context():
    db.create_all()

from .tasks import views
from .auth import views, auth_app

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Необходима авторизация!'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
