from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    email = StringField("Your Email", validators=[DataRequired(), Email()])
    username = StringField("Username")
    message = TextAreaField(
        "Message", render_kw={"style": "height: 20ch"}, validators=[DataRequired()]
    )
