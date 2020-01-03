from init import db
from models import Questions, Answers, Users
from datetime import datetime
from config import update_rating


def get_current_datetime():
    return datetime.now().strftime('%d-%m-%Y %H:%M')


def add_question(username, text, answer, is_one_attempt, score):
    question = Questions(creator=username, text=text, time=get_current_datetime(), correct_answer=answer,
                         one_attempt=is_one_attempt, score=score, total_answers=0)
    db.session.add(question)
    db.session.commit()


def is_correct_answer(question_id, text):
    question = get_question(question_id)
    return question.correct_answer == text


def is_answered(username, question_id):
    result = Answers.query.filter(Answers.question_id == question_id, Answers.username == username,
                                  Answers.status == 'Active').first()
    return result is not None


def is_used_question(username, question_id):
    result = Answers.query.filter(Answers.question_id == question_id, Answers.username == username).first()
    return result is not None


def write_answer(username, question_id, text, user_score):
    is_correct = is_correct_answer(question_id, text)
    question = get_question(question_id)

    if is_correct and not is_used_question(username, question_id) and question.creator != username:
        user = get_user(username)
        user.score += question.score
        db.session.commit()

    answer = Answers(username=username, question_id=question_id, answer=text, time=get_current_datetime(),
                     is_correct=is_correct, user_scored=user_score)
    question.total_answers += 1
    db.session.add(answer)
    db.session.commit()
    update_question_score(question_id, user_score)


def register_user(username, email, password):
    user = Users(username=username, email=email, score=0)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


def get_user(username):
    return Users.query.filter_by(username=username).first()


def get_questions_list(author=None, text=None, status=None):
    questions_list = Questions.query
    if author is not None:
        questions_list = questions_list.filter(Questions.creator == author)
    if text is not None:
        questions_list = questions_list.filter(Questions.text.like('%{}%'.format(text)))
    if status is not None:
        questions_list = questions_list.filter(Questions.status == status)
    return questions_list.all()


def get_answers_list(questions_owner, answered_by=None, question_text=None, status=None):
    answers_list = Answers.query.join(Questions, Answers.question_id == Questions.id).add_columns(
        Questions.text, Questions.creator, Questions.correct_answer, Questions.score)

    if questions_owner is not None:
        answers_list = answers_list.filter(Questions.creator == questions_owner)

    if answered_by is not None:
        answers_list = answers_list.filter(Answers.username == answered_by)

    if question_text is not None:
        answers_list = answers_list.filter(Questions.text.like('%{}%'.format(question_text)))

    if status is not None:
        answers_list = answers_list.filter(Answers.status == status)

    return answers_list.all()


def get_question(question_id):
    return Questions.query.filter(Questions.id == question_id).first()


def get_answer(answer_id):
    return Answers.query.filter(Answers.id == answer_id).first()


def delete_question(question_id):
    db.session.delete(get_question(question_id))
    db.session.commit()


def delete_answer(answer_id):
    db.session.delete(get_answer(answer_id))
    db.session.commit()


def archive_answer(answer_id):
    answer = get_answer(answer_id)
    answer.status = 'Archived'
    db.session.commit()


def archive_question(question_id):
    question = get_question(question_id)
    question.status = 'Archived'
    db.session.commit()


def update_question_score(question_id, user_score):
    question = get_question(question_id)
    score = update_rating(question.score, user_score)
    question.score = score
    db.session.commit()


def get_users_scores():
    users_list = Users.query.order_by(db.desc(Users.score)).all()
    return users_list
