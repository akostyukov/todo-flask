from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

from app import app
from app.forms import UserForm
from app.models import User, db


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = UserForm(request.form)

        if form.validate_on_submit():
            user_login = form.login.data
            user_password = form.password.data
        else:
            return redirect(url_for('login'))

        user = User.query.filter_by(login=user_login).first()

        if not user or not user.check_password(user_password):
            flash('Ошибка авторизации!')
            return redirect(url_for('login'))

        flash(f'Привет, {user.login}!')
        login_user(user, remember=True)
        return redirect(url_for('task_list'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('task_list'))

        return render_template(
            'auth/login.html',
            users=User.query.all(),
            form=UserForm()
        )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = UserForm(request.form)

        if form.validate_on_submit():
            db.session.add(User(form.login.data, form.password.data))
        else:
            return redirect(url_for('register'))

        try:
            db.session.commit()
        except IntegrityError:
            flash("Пользователь с таким логином существует!")
            return redirect(url_for('register'))

        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('login'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('task_list'))

        return render_template('auth/register.html', form=UserForm())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
