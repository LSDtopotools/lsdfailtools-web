from .application import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    profile_pic = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.id)
