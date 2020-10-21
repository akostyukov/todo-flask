from flask_login import UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, task, user_id):
        self.task = task
        self.user_id = user_id

    def set_done(self):
        self.status = False
        db.session.commit()

    def delete_task(self):
        db.session.delete(Task.query.get(self.id))
        db.session.commit()

    @staticmethod
    def clear_all():
        db.session.query(Task).filter(Task.user_id == current_user.id).delete()
        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Task')

    def __init__(self, login, password):
        self.login = login
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return True if check_password_hash(self.password, password) else False
