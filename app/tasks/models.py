from flask_login import current_user

from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, task, user_id):
        self.task = task
        self.user_id = user_id

    def set_done(self):
        self.status = False
        db.session.commit()

    def delete_task(self):
        db.session.delete(Task.query.get(self.id))
        db.session.commit()

    @staticmethod
    def clear_all():
        db.session.query(Task).filter(Task.user_id == current_user.id).delete()
        db.session.commit()
