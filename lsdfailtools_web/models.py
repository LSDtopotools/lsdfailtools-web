from .application import db
from flask_login import UserMixin
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=True)
    profile_pic = db.Column(db.Text, nullable=True)
    runs = relationship("Run", back_populates="user")

    def __repr__(self):
        return '<User {}>'.format(self.id)


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    see https://docs.sqlalchemy.org/en/13/core/custom_types.html#backend-agnostic-guid-type  # noqa E501

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class RunState(Enum):
    new = 1
    running = 2
    complete = 3
    failed = 4


class Run(db.Model):
    __tablename__ = 'runs'
    id = db.Column(GUID, primary_key=True)
    submitted = db.Column(db.DateTime)
    status = db.Column(db.Enum(RunState))
    user_id = db.Column(db.Text, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="runs")


def jsonify_run(runs):
    result = []
    for run in runs:
        actual_run = {}
        actual_run['id'] = str(run.id)
        actual_run['status'] = str(run.status)
        result.append(actual_run)
    return result
