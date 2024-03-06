from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from constants import (MAX_USERNAME_LENGTH, MAX_PSW_LENGTH, MAX_EMAIL_LENGTH,
    MAX_FIRSTNAME_LENGTH, MAX_LASTNAME_LENGTH, MAX_NOTE_TITLE_LENGTH)

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to the database"""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Model for user"""

    __tablename__ = 'users'

    notes = db.relationship('Note', backref='user')

    username = db.Column(
        db.String(MAX_USERNAME_LENGTH),
        primary_key=True
    )

    hashed_password = db.Column(
        db.String(MAX_PSW_LENGTH),
        nullable=False
    )

    email = db.Column(
        db.String(MAX_EMAIL_LENGTH),
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.String(MAX_FIRSTNAME_LENGTH),
        nullable=False
    )

    last_name = db.Column(
        db.String(MAX_LASTNAME_LENGTH),
        nullable=False
    )

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """ Register new user with hashed password and user info """

        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')

        return cls(
            username=username,
            hashed_password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.
        Return user if valid; else return False.
        """

        u = cls.query.get(username)
        if u and bcrypt.check_password_hash(u.hashed_password, pwd):
            return u
        else:
            return False


class Note(db.Model):
    """Model for notes"""

    __tablename__ = 'notes'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(MAX_NOTE_TITLE_LENGTH),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    owner_username = db.Column(
        db.String(MAX_USERNAME_LENGTH),
        db.ForeignKey('users.username'),
        nullable = False
    )
