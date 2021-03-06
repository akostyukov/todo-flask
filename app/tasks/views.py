from flask import redirect, url_for
from flask.views import MethodView
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


class DeleteTaskView(MethodView):
    decorators = [login_required]

    @staticmethod
    def get(task_id):
        task = Task.query.get(task_id)

        if task.user_id == current_user.id:
            Task.query.get(task_id).delete_task()
        return redirect(url_for('task_list'))


class DoneTaskView(MethodView):
    decorators = [login_required]

    @staticmethod
    def get(task_id):
        task = Task.query.get(task_id)

        if task.user_id == current_user.id:
            Task.query.get(task_id).set_done()
        return redirect(url_for('task_list'))


class ClearTasksView(MethodView):
    decorators = [login_required]

    def get(self):
        Task.clear_all()
        return redirect(url_for('task_list'))


app.add_url_rule('/', view_func=TaskView.as_view('task_list'))
app.add_url_rule('/done/<int:task_id>', view_func=DoneTaskView.as_view('do_task'))
app.add_url_rule('/delete/<int:task_id>', view_func=DeleteTaskView.as_view('delete_task'))
app.add_url_rule('/clear', view_func=ClearTasksView.as_view('clear'))
