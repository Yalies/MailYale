import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'sqlite:///' + os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CAS_SERVER = 'https://secure.its.yale.edu'
    CAS_AFTER_LOGIN = 'index'
    CAS_LOGIN_ROUTE = '/cas/login'
    CAS_AFTER_LOGOUT = 'index'
