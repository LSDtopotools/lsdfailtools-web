__all__ = ['Config']

from pathlib import Path
import os


class Config:
    BASEDIR = os.environ.get('LFT_BASEDIR') or '/tmp/lsdfailtools'
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max-limit
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + str(Path(BASEDIR) / 'lsdfailtools_web.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration")

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL") or \
        'amqp://guest@localhost//'
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND") or \
        'amqp://guest@localhost//'
