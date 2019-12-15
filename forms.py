from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange

from models import Users
import config


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AnswerForm(FlaskForm):
    answer_text = TextAreaField('AnswerText', validators=[DataRequired()])
    user_score = IntegerField('User score', validators=[DataRequired(),
                                                        NumberRange(config.MARK_RANGE_MIN, config.MARK_RANGE_MAX)])


class QuestionsAddingForm(FlaskForm):
    question = TextAreaField('Question', validators=[DataRequired()])
    answer = TextAreaField('Answer', validators=[DataRequired()])
    is_one_attempt = BooleanField('IsOneAttempt')
    initial_score = IntegerField('Initial score', validators=[DataRequired(), NumberRange(config.MARK_RANGE_MIN,
                                                                                          config.MARK_RANGE_MAX)])


class FilterForm(FlaskForm):
    creator = TextAreaField('Name')
    text = TextAreaField('Text')
