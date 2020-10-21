from flask_login import current_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

from app import db
from .models import User, Task


class TaskForm(FlaskForm):
    task = StringField(validators=[DataRequired(), Length(min=1, max=30)], render_kw={'autofocus': True})

    def save(self):
        db.session.add(Task(self.task.data, current_user.id))
        db.session.commit()


class UserForm(FlaskForm):
    login = StringField(validators=[DataRequired(), Length(min=4, max=15)], render_kw={'autofocus': True})
    password = PasswordField(validators=[DataRequired(), Length(min=4, max=20)])

    def save(self):
        db.session.add(User(self.login.data, self.password.data))
        db.session.commit()
        # login_user(user, remember=True)
