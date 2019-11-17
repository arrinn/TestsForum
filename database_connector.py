from init import db
from models import Questions, Answers, Users


def add_question(username, text):
    question = Questions(creator=username, text=text)
    db.session.add(question)
    db.session.commit()


def write_answer(username, question_id, text):
    answer = Answers(username=username, question_id=question_id, answer=text)
    db.session.add(answer)
    db.session.commit()


def register_user(username, email, password):
    user = Users(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


def get_user(username):
    return Users.query.filter_by(username=username).first()


def get_questions_list():
    questions_list = Questions.query.all()
    return questions_list
