from flask import flash, redirect, request
from flask import render_template, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from init import app
from forms import LoginForm, AnswerForm, RegistrationForm, QuestionsAddingForm, FilterForm

from database_connector import get_questions_list, write_answer, register_user, get_user, add_question, \
    get_answers_list, delete_question, get_question, is_answered, get_answer, archive_answer


@app.route('/index')
def hello_world():
    username = current_user.username if current_user.is_authenticated else 'None'
    return render_template("index.html", title='Home', username=username)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/index')

    form = RegistrationForm()
    if form.validate_on_submit():
        register_user(form.username.data, form.email.data, form.password.data)
        return redirect('/login')

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')

    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.username.data)

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = '/index'
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')


@app.route('/questions', methods=['GET', 'POST', 'UPDATE'])
@login_required
def questions():
    filter_form = FilterForm()
    creator = request.args.get('creator', None)
    text = None
    if request.method == 'POST' and filter_form.validate_on_submit():
        creator = filter_form.creator.data if filter_form.creator.data else None
        text = filter_form.text.data if filter_form.text.data else None

    return render_template('questions.html', questions=get_questions_list(creator, text), form=AnswerForm(),
                           current_user=current_user.username, filter_form=filter_form)


@app.route('/answer/<question_id>', methods=['POST'])
@login_required
def answer_question(question_id):
    answer_form = AnswerForm()
    if answer_form.validate_on_submit():
        if not is_answered(current_user.username, question_id) or not get_question(question_id).one_attempt:
            write_answer(current_user.username, question_id, answer_form.answer_text.data, answer_form.user_score.data)
    return redirect(url_for('questions'))


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', username=current_user.username)


@app.route('/answers', methods=['GET', 'POST'])
@login_required
def answers_list():
    filter_form = FilterForm()
    if request.method == 'POST' and filter_form.validate_on_submit():
        answered_by_filter = filter_form.creator.data if filter_form.creator.data else None
        question_text_filter = filter_form.text.data if filter_form.text.data else None
        answers = get_answers_list(questions_owner=current_user.username, answered_by=answered_by_filter,
                                   question_text=question_text_filter, status='Active')
    else:
        answers = get_answers_list(questions_owner=current_user.username, status='Active')
    return render_template('answers.html', answers=answers, filter_form=filter_form, is_my_answers=False)


@app.route('/my_answers', methods=['GET', 'POST'])
@login_required
def my_answers_view():
    filter_form = FilterForm()
    if request.method == 'POST' and filter_form.validate_on_submit():
        creator_filter = filter_form.creator.data if filter_form.creator.data else None
        question_text_filter = filter_form.text.data if filter_form.text.data else None
        answers = get_answers_list(questions_owner=creator_filter, answered_by=current_user.username,
                                   question_text=question_text_filter, status='Active')
    else:
        answers = get_answers_list(questions_owner=None, answered_by=current_user.username, status='Active')
    return render_template('answers.html', answers=answers, filter_form=filter_form, is_my_answers=True)


@app.route('/add_question', methods=['GET', 'POST'])
@login_required
def add_question_view():
    form = QuestionsAddingForm()
    if request.method == 'POST' and form.validate_on_submit():
        add_question(current_user.username, form.question.data, form.answer.data, form.is_one_attempt.data,
                     form.initial_score.data)
        return redirect('/questions')
    else:
        return render_template('add_question.html', form=form)


@app.route('/delete/<question_id>', methods=['POST'])
@login_required
def delete_question_view(question_id):
    if get_question(question_id).creator == current_user.username:
        delete_question(question_id)
    return redirect('/questions')


@app.route('/delete_answer/<answer_id>', methods=['POST'])
@login_required
def delete_answer_view(answer_id):
    if get_answer(answer_id).username == current_user.username:
        archive_answer(answer_id)
    return redirect('/my_answers')


if __name__ == '__main__':
    app.run(debug=True)
