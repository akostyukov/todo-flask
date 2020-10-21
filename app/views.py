from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app import app
from app.auth import FormView
from app.forms import TaskForm
from app.models import Task, db


class TaskView(FormView):
    decorators = [login_required]

    template = 'index.html'
    success_url = 'task_list'
    fail_url = 'task_list'
    form = TaskForm

    def get_context(self):
        return {
            'form': TaskForm(),
            'tasks': Task.query.filter_by(status=True, user_id=current_user.id).all()[::-1],
            'done_tasks': Task.query.filter_by(status=False, user_id=current_user.id).all(),
        }

    def post(self):
        return super().post()


class DeleteTaskView(FormView):
    decorators = [login_required]

    def get(self, task_id):
        task = Task.query.get(task_id)

        if task.user_id == current_user.id:
            Task.query.get(task_id).delete_task()
        return redirect(url_for('task_list'))


class DoneTaskView(FormView):
    decorators = [login_required]

    def get(self, task_id):
        task = Task.query.get(task_id)

        if task.user_id == current_user.id:
            Task.query.get(task_id).set_done()
        return redirect(url_for('task_list'))


class ClearTasksView(FormView):
    decorators = [login_required]

    def get(self):
        Task.clear_all()
        return redirect(url_for('task_list'))


app.add_url_rule('/', view_func=TaskView.as_view('task_list'))
app.add_url_rule('/done/<int:task_id>', view_func=DoneTaskView.as_view('do_task'))
app.add_url_rule('/delete/<int:task_id>', view_func=DeleteTaskView.as_view('delete_task'))
app.add_url_rule('/clear', view_func=ClearTasksView.as_view('clear'))
