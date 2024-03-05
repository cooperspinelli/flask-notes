from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, Email

# TODO: Make a file constants.py for input length to validtate on the form level as well

class RegisterForm(FlaskForm):
    """Form for registering"""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6)]
    )

    email = EmailField(
        "Email",
        validators=[InputRequired(), Email()]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired()]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired()]
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
        validators=[InputRequired()]
    )

    content = StringField(
        "Content",
        validators=[InputRequired()]
    )


class CSRFProtectForm(FlaskForm):
    """ Form for CSRF protection """
