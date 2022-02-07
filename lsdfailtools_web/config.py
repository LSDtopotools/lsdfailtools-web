__all__ = ['Config']

from pathlib import Path
import os


class Config:
    BASEDIR = os.environ.get('LFT_BASEDIR') or '/tmp/lsdfailtools'
    ADMIN = os.environ.get('LFT_ADMIN') or 'magnus.hagdorn@ed.ac.uk'
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max-limit
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + str(Path(BASEDIR) / 'lsdfailtools_web.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    if 'SERVER_NAME' in os.environ:
        SERVER_NAME = os.environ.get('SERVER_NAME')

    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration")

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL") or \
        'amqp://guest@localhost//'
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND") or \
        'amqp://guest@localhost//'

    RESULT_NAME = 'landslide_failures_output.zip'
    LSDFAILTOOL = os.environ.get('LSDFAILTOOL') or 'lsdfailtools-wrapper'
    LSDFAILTOOL_CFG = os.environ.get('LSDFAILTOOL_CFG') or \
        'file_paths_landslide_automation.json'

    WORK_END_ENDPOINT = os.environ.get('WORK_END_ENDPOINT') or \
        'localhost/api/integration/ed/finish/work/'
