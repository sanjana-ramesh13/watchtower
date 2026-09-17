from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, URL
from wtforms.form import Form
from models import User

class SignupForm(Form):
    """Form for user registration"""
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=20, message='Username must be 3-20 characters')
        ]
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Invalid email address')
        ]
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required'),
            Length(min=6, message='Password must be at least 6 characters')
        ]
    )
    
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message='Please confirm your password'),
            EqualTo('password', message='Passwords must match')
        ]
    )
    
    submit = SubmitField('Sign Up')
    
    def validate_username(self, field):
        """Check if username already exists"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')
    
    def validate_email(self, field):
        """Check if email already exists"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')


class LoginForm(Form):
    """Form for user login"""
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Invalid email address')
        ]
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required')
        ]
    )
    
    submit = SubmitField('Log In')


class AddWebsiteForm(Form):
    """Form for adding a website to monitor"""
    name = StringField(
        'Website Name',
        validators=[
            DataRequired(message='Website name is required'),
            Length(min=1, max=120, message='Name must be 1-120 characters')
        ]
    )
    
    url = StringField(
        'Website URL',
        validators=[
            DataRequired(message='URL is required'),
            URL(message='Invalid URL format')
        ]
    )
    
    submit = SubmitField('Add Website')
