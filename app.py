from flask import flash, redirect, request
from flask import render_template, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from init import app
from forms import LoginForm, AnswerForm, RegistrationForm, QuestionsAddingForm

from database_connector import get_questions_list, write_answer, register_user, get_user, add_question


@app.route('/')
@app.route('/index')
def hello_world():
    user = {'nickname': current_user.username}
    return render_template("index.html", title='Home', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/index')

    form = RegistrationForm()
    if form.validate_on_submit():
        register_user(form.username.data, form.email.data, form.password.data)
        flash('Congratulations, you are now a registered user!')
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


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    adding_form = QuestionsAddingForm()

    if request.method == "POST":
        add_question(current_user.username, adding_form.text.data)

    form = AnswerForm()
    return render_template('questions.html', questions=get_questions_list(), form=form, adding_form=adding_form)


@app.route('/answer/<question_id>', methods=['POST'])
def answer_question(question_id):
    answer_text = request.form['answer']
    write_answer(current_user.username, question_id, answer_text)
    return redirect(url_for('questions'))


if __name__ == '__main__':
    app.run(debug=True)
