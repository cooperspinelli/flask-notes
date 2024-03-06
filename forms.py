from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, Email
from constants import (MAX_USERNAME_LENGTH, MAX_EMAIL_LENGTH,
    MAX_FIRSTNAME_LENGTH, MAX_LASTNAME_LENGTH, MAX_NOTE_TITLE_LENGTH)


class RegisterForm(FlaskForm):
    """Form for registering"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=MAX_USERNAME_LENGTH)]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6)]
    )

    email = EmailField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=MAX_EMAIL_LENGTH)]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(max=MAX_FIRSTNAME_LENGTH)]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=MAX_LASTNAME_LENGTH)]
    )


class LoginForm(FlaskForm):
    """Form for logging in"""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )


class AddNoteForm(FlaskForm):
    """ Form for adding a note """

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=MAX_NOTE_TITLE_LENGTH)]
    )

    # listen to gracee
    content = StringField(
        "Content",
        validators=[InputRequired()]
    )


class CSRFProtectForm(FlaskForm):
    """ Form for CSRF protection """
