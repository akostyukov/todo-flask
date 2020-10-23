from flask import flash
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

from .models import User
from app.decorators import commit_transaction
from app import db


class UserForm(FlaskForm):
    login = StringField(validators=[DataRequired(), Length(min=4, max=15)], render_kw={'autofocus': True})
    password = PasswordField(validators=[DataRequired(), Length(min=4, max=20)])


class LoginForm(UserForm):
    def save(self):
        user = User.query.filter_by(login=self.login.data).first()

        if not user or not user.check_password(self.password.data):
            flash('Ошибка авторизации!')
            raise Exception
        else:
            flash(f'Привет, {user.login}!')
            login_user(user, remember=True)


class RegisterForm(UserForm):
    @commit_transaction
    def save(self):
        db.session.add(User(self.login.data, self.password.data))
