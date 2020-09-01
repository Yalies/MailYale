import os
basedir = os.path.abspath(os.path.dirname(__file__))


REDIS = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Override this in production')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'Override this too')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'sqlite:///' + os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = REDIS
    CELERY_RESULT_BACKEND = REDIS
