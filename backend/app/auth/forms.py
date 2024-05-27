import re

from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileRequired
from password_strength import PasswordStats
from wtforms import (
    BooleanField,
    FileField,
    FormField,
    HiddenField,
    IntegerField,
    PasswordField,
    StringField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    InputRequired,
    Length,
    Optional,
    ValidationError,
)
from wtforms_sqlalchemy.fields import QuerySelectField

from app.auth.password import validate_policy
from app.models import User


class UserCheck(object):
    def __init__(self, banned, regex, message=None):
        self.banned = banned
        self.regex = regex

        if not message:
            message = "Please choose another username"
        self.message = message

    def __call__(self, form, field):
        p = re.compile(self.regex)
        if field.data.lower() in (word.lower() for word in self.banned):
            raise ValidationError(self.message)
        if re.search(p, field.data.lower()):
            raise ValidationError(self.message)


class PasswordResetReqestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])

    def validate_email(self, email):
        user = User.query.filter(User.email.ilike(email.data)).first()
        if user is None:
            raise ValidationError("No user found with this email.")


class PasswordResetForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    token = HiddenField("token", validators=[DataRequired()])

    def validate_password(self, password):
        stats = PasswordStats(password.data)
        if stats.strength() < 0.3:
            raise ValidationError("Password too weak.")
        errors = validate_policy(password.data)
        if errors is not None:
            raise ValidationError(errors)


class LoginForm(FlaskForm):
    identifier = StringField("Email or Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")


class SignupForm(FlaskForm):
    username = StringField(
        "Username (This will appear in your URL for your public page and will be used for logging in.)",
        validators=[
            DataRequired(),
            UserCheck(
                message="Username or special characters not allowed",
                banned=["root", "admin", "sys", "administrator"],
                regex="^(?=.*[-+_!@#$%^&*., ?])",
            ),
        ],
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )

    def validate_username(self, username):
        if isinstance(username, str):
            user = User.query.filter(User.username.ilike(username)).first()
            if user is not None:
                return "Username already taken."
        else:
            user = User.query.filter(User.username.ilike(username.data)).first()
            if user is not None:
                raise ValidationError("Username already taken.")

    def validate_email(self, email):
        if isinstance(email, str):
            user = User.query.filter(User.email.ilike(email)).first()
            if user is not None:
                return "Email already registered."
        else:
            user = User.query.filter(User.email.ilike(email.data)).first()
            if user is not None:
                raise ValidationError("Email already registered.")

    def validate_password(self, password):
        stats = PasswordStats(password.data)
        if stats.strength() < 0.3:
            raise ValidationError("Password too weak.")
        errors = validate_policy(password.data)
        if errors is not None:
            raise ValidationError(errors)
