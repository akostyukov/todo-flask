from flask import Flask

from app.models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'dev'
db.init_app(app)

with app.app_context():
    db.create_all()

from app import views
