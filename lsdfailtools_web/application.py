from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

csrf = CSRFProtect()

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

csrf.init_app(app)
