from flask import redirect, url_for
from flask_login import login_required, logout_user, current_user

from app import app
from app.auth.forms import LoginForm, RegisterForm
from app.forms import FormView


class LoginView(FormView):
    form = LoginForm
    template = 'login.html'
    success_url = 'task_list'
    fail_url = 'login'

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('task_list'))

        return super().get()


class RegisterView(FormView):
    form = RegisterForm
    template = 'register.html'
    success_url = 'login'
    fail_url = 'register'

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('task_list'))

        return super().get()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/register', view_func=RegisterView.as_view('register'))
