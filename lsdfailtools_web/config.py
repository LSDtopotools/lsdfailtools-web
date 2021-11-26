__all__ = ['Config']

from pathlib import Path
import os

basedir = Path('/tmp')


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + str(basedir / 'lsdfailtools_web.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
