from init import db
from models import Questions, Answers, Users
from datetime import datetime


def get_current_datetime():
    return datetime.now().strftime('%d-%m-%Y %H:%M')


def add_question(username, text, answer):
    question = Questions(creator=username, text=text, time=get_current_datetime())
    db.session.add(question)
    db.session.commit()


def write_answer(username, question_id, text):
    answer = Answers(username=username, question_id=question_id, answer=text, time=get_current_datetime())
    db.session.add(answer)
    db.session.commit()


def register_user(username, email, password):
    user = Users(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


def get_user(username):
    return Users.query.filter_by(username=username).first()


def get_questions_list(author):
    if author is None:
        questions_list = Questions.query.all()
    else:
        questions_list = Questions.query.filter(Questions.creator == author).all()
    return questions_list


def get_answers_list(questions_owner):
    questions_list = get_questions_list(questions_owner)
    answers = Answers.query.join(Questions, Answers.question_id == Questions.id)\
        .add_columns(Questions.text, Questions.creator).all()
    return answers


def get_question(question_id):
    return Questions.query.filter(Questions.id == question_id).first()


def delete_question(question_id):
    db.session.delete(get_question(question_id))
    db.session.commit()
