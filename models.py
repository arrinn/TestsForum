from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from init import db, login


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    answers = db.relationship('Answers', backref='answered', lazy='dynamic')
    questions = db.relationship('Questions', backref='created', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.String(64), db.ForeignKey('users.username'))
    text = db.Column(db.String(120))
    time = db.Column(db.String(32))

    def __repr__(self):
        return '<id: {}, text: {}>'.format(self.id, self.text)


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    username = db.Column(db.String(64), db.ForeignKey('users.username'))
    answer = db.Column(db.String(120))
    time = db.Column(db.String(32))

    def __repr__(self):
        return '<id: {}, question_id: {}, user_id: {}, text: {}>'.format(
            self.id, self.question_id, self.user_id, self.text)
