from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

from app import app
from app.models import User, db


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_login = request.form['login']
        user_password = request.form['password']
        user = User.query.filter_by(login=user_login).first()

        if not user or user.password != user_password:
            flash('Ошибка авторизации!')
            return redirect(url_for('login'))

        login_user(user, remember=True)
        return redirect(url_for('task_list'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('task_list'))

        return render_template(
            'auth/login.html',
            users=User.query.all()
        )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db.session.add(User(request.form['login'], password=request.form['password']))
        try:
            db.session.commit()
        except IntegrityError:
            flash("Пользователь с таким логином существует!")
            return redirect(url_for('register'))
        return redirect(url_for('login'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('task_list'))

        return render_template('auth/register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
