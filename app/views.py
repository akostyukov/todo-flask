from flask import render_template, request, redirect, url_for

from app import app
from app.models import Task, db


@app.route('/')
def task_list():
    return render_template(
        'index.html',
        tasks=Task.query.filter_by(status=True).all()[::-1],
        done_tasks=Task.query.filter_by(status=False).all()
    )


@app.route('/add', methods=['POST'])
def add_task():
    db.session.add(Task(request.form['task']))
    db.session.commit()
    return redirect(url_for('task_list'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    db.session.delete(Task.query.get(task_id))
    db.session.commit()
    return redirect(url_for('task_list'))


@app.route('/clear')
def clear():
    db.session.query(Task).delete()
    db.session.commit()
    return redirect(url_for('task_list'))


@app.route('/done/<int:task_id>')
def done(task_id):
    Task.query.get(task_id).status = False
    db.session.commit()
    return redirect(url_for('task_list'))
