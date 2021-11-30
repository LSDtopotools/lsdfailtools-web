from .application import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    profile_pic = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.id)
