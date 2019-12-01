from init import db
from models import Questions, Answers, Users
from datetime import datetime


def get_current_datetime():
    return datetime.now().strftime('%d-%m-%Y %H:%M')


def add_question(username, text, answer, is_one_attempt):
    question = Questions(creator=username, text=text, time=get_current_datetime(), correct_answer=answer,
                         one_attempt=is_one_attempt)
    db.session.add(question)
    db.session.commit()


def is_correct_answer(question_id, text):
    question = get_question(question_id)
    return question.correct_answer == text


def is_answered(username, question_id):
    result = Answers.query.filter(question_id == question_id, username == username).first()
    return result is not None


def write_answer(username, question_id, text):
    answer = Answers(username=username, question_id=question_id, answer=text, time=get_current_datetime(),
                     is_correct=is_correct_answer(question_id, text))
    db.session.add(answer)
    db.session.commit()


def register_user(username, email, password):
    user = Users(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


def get_user(username):
    return Users.query.filter_by(username=username).first()


def get_questions_list(author=None, text=None):
    questions_list = Questions.query
    if author is not None:
        questions_list = questions_list.filter(Questions.creator == author)
    if text is not None:
        questions_list = questions_list.filter(Questions.text.like('%{}%'.format(text)))
    return questions_list.all()


def get_answers_list(questions_owner, answered_by=None, question_text=None):
    answers_list = Answers.query.join(Questions, Answers.question_id == Questions.id).add_columns(
        Questions.text, Questions.creator, Questions.correct_answer)

    if questions_owner is not None:
        answers_list = answers_list.filter(Questions.creator == questions_owner)

    if answered_by is not None:
        answers_list = answers_list.filter(Answers.username == answered_by)

    if question_text is not None:
        answers_list = answers_list.filter(Questions.text.like('%{}%'.format(question_text)))

    return answers_list.all()


def get_question(question_id):
    return Questions.query.filter(Questions.id == question_id).first()


def delete_question(question_id):
    db.session.delete(get_question(question_id))
    db.session.commit()
