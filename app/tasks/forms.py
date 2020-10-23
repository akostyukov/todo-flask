from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from app.decorators import commit_transaction
from app.tasks.models import Task, db


class TaskForm(FlaskForm):
    task = StringField(validators=[DataRequired(), Length(min=1, max=30)], render_kw={'autofocus': True})

    @commit_transaction
    def save(self):
        db.session.add(Task(self.task.data, current_user.id))