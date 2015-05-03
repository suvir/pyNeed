__author__ = 'suvir'
from werkzeug import generate_password_hash, check_password_hash


def get_password_hash(password):
    return generate_password_hash(password)


def check_password(pwdhash, password):
    return check_password_hash(pwdhash, password)

