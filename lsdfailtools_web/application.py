from flask import Flask, has_app_context
from flask_wtf.csrf import CSRFProtect
from celery import Celery
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# handle celery task creation and teardown
# see https://stackoverflow.com/questions/12044776/how-to-use-flask-sqlalchemy-in-a-celery-task  # noqa E501
class FlaskCelery(Celery):

    def __init__(self, *args, **kwargs):

        super(FlaskCelery, self).__init__(*args, **kwargs)
        self.patch_task()

        if 'app' in kwargs:
            self.init_app(kwargs['app'])

    def patch_task(self):
        TaskBase = self.Task
        _celery = self

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                if has_app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
                else:
                    with _celery.app.app_context():
                        return TaskBase.__call__(self, *args, **kwargs)

        self.Task = ContextTask

    def init_app(self, app):
        self.app = app
        self.config_from_object(app.config)


csrf = CSRFProtect()

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

csrf.init_app(app)

celery = FlaskCelery()
celery.init_app(app)
celery.conf.update(app.config)
