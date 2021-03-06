import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = True
CSRF_ENABLED = True
SECRET_KEY = '13543acb54b34ce54'

MARK_RANGE_MIN = 1
MARK_RANGE_MAX = 10
EMA_ALPHA = 0.25


def update_rating(current_score, user_score):
    return round(EMA_ALPHA * user_score + (1 - EMA_ALPHA) * current_score, 2)
