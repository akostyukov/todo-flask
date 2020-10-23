from flask import redirect, url_for
from flask_login import login_required, current_user

from app import app
from app.forms import FormView
from .forms import TaskForm
from .models import Task


class TaskView(FormView):
    decorators = [login_required]

    template = 'index.html'
    success_url = 'task_list'
    fail_url = 'task_list'
    form = TaskForm

    def get_context(self):
        return {
            'tasks': Task.query.filter_by(status=True, user_id=current_user.id).all()[::-1],
            'done_tasks': Task.query.filter_by(status=False, user_id=current_user.id).all(),
        }

    def post(self):
        return super().post()


class DeleteTaskView:
    decorators = [login_required]

    @staticmethod
    @app.route('/delete/<int:task_id>')
    def delete_task(task_id):
        task = Task.query.get(task_id)

        if task.user_id == current_user.id:
            Task.query.get(task_id).delete_task()
        return redirect(url_for('task_list'))


class DoneTaskView:
    decorators = [login_required]

    @staticmethod
    @app.route('/done/<int:task_id>')
    def do_task(task_id):
        task = Task.query.get(task_id)

        if task.user_id == current_user.id:
            Task.query.get(task_id).set_done()
        return redirect(url_for('task_list'))


class ClearTasksView:
    decorators = [login_required]

    @staticmethod
    @app.route('/clear')
    def clear():
        Task.clear_all()
        return redirect(url_for('task_list'))


app.add_url_rule('/', view_func=TaskView.as_view('task_list'))
