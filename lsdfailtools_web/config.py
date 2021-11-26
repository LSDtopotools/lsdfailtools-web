__all__ = ['Config']

import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dhdtPy-is-not-so-secret'
