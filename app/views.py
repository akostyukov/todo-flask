from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app import app
from app.forms import TaskForm
from app.models import Task, db


@app.route('/')
@login_required
def task_list():
    return render_template(
        'index.html',
        tasks=Task.query.filter_by(status=True, user_id=current_user.id).all()[::-1],
        done_tasks=Task.query.filter_by(status=False, user_id=current_user.id).all(),
        form=TaskForm()
    )


@app.route('/add', methods=['POST'])
@login_required
def add_task():
    form = TaskForm(request.form)

    if form.validate_on_submit():
        db.session.add(Task(form.task.data, current_user.id))
        db.session.commit()

    return redirect(url_for('task_list'))


@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task.user_id == current_user.id:
        db.session.delete(Task.query.get(task_id))
        db.session.commit()

    return redirect(url_for('task_list'))


@app.route('/clear')
@login_required
def clear():
    db.session.query(Task).filter(Task.user_id == current_user.id).delete()
    db.session.commit()
    return redirect(url_for('task_list'))


@app.route('/done/<int:task_id>')
@login_required
def done(task_id):
    if Task.query.get(task_id).user_id == current_user.id:
        Task.query.get(task_id).status = False
        db.session.commit()
    return redirect(url_for('task_list'))
