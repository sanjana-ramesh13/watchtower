from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, URLField
from wtforms.validators import DataRequired, Email, Length, URL

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(min=5, max=120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    submit = SubmitField('Login')

class AddWebsiteForm(FlaskForm):
    url = URLField('Website URL', validators=[
        DataRequired(),
        URL(),
        Length(min=10, max=500)
    ])
    submit = SubmitField('Add Website')
