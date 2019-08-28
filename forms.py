from wtforms import StringField, PasswordField, IntegerField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired


class CreateUserForm(FlaskForm):
    """Form for creating a new user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form for creating a new user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class FeedbackForm(FlaskForm): 
    """Form for feedback""" 

    title = StringField("Title", validators=[InputRequired()])
    feedback = TextAreaField("Feedback", validators=[InputRequired()])
    