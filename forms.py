from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, URLField
from wtforms.validators import DataRequired, Email, Length, URL

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddWebsiteForm(FlaskForm):
    url = URLField('Website URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Add Website')
