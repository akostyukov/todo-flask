from flask import render_template, request, redirect, url_for, flash
from flask.views import MethodView
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

from app import app
from app.forms import UserForm
from app.models import User, db


class FormView(MethodView):
    form = None
    success_url = ''
    fail_url = ''

    def get_context(self):
        return {}

    def get(self, request):
        return render_template(self.form, **self.get_context())

    def post(self, request):
        form = self.form(request.form)

        if form.validate_on_submit():
            form.process()
            form.save()
            return redirect(self.success_url)
        return redirect(self.fail_url)


# @app.route('/v1/login', methods=['GET', 'POST'])
class LoginView(FormView):
    def get_context(self):
        return {'users': User.query.all()}

    def post(self, request):
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

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('task_list'))

        super().get(0)


class RegisterView(FormView):
    form = UserForm()

    # @app.route('/register', methods=['GET', 'POST'])
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('task_list'))

        return super().get()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


app.route('/login', methods=['GET', 'POST'])(LoginView.as_view())
app.route('/register', methods=['GET', 'POST'])(RegisterView.as_view())
