from app import db


def commit_transaction(func):
    def wrapped(self):
        func(self)
        db.session.commit()

    return wrapped
