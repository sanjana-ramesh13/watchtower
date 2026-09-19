from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, URLField
from wtforms.validators import DataRequired, Email, Length, Regexp, URL, ValidationError
from models import User

class SignupForm(FlaskForm):
    """Form for user registration with strong password requirements"""
    
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address'),
        Length(min=5, max=120, message='Email must be between 5 and 120 characters')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters'),
        Regexp(
            r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)',
            message='Password must contain uppercase letter, lowercase letter, and number'
        )
    ])
    
    submit = SubmitField('Sign Up')
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please login or use a different email.')


class LoginForm(FlaskForm):
    """Form for user login"""
    
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])
    
    remember_me = BooleanField('Remember Me')
    
    submit = SubmitField('Login')


class AddWebsiteForm(FlaskForm):
    """Form for adding a website to monitor"""
    
    url = URLField('Website URL', validators=[
        DataRequired(message='URL is required'),
        URL(message='Invalid URL. Must start with http:// or https://'),
        Length(min=10, max=500, message='URL must be between 10 and 500 characters')
    ])
    
    submit = SubmitField('Add Website')
    
    def validate_url(self, url):
        """Validate URL format and check for duplicates"""
        # Ensure URL starts with http:// or https://
        url_value = url.data.strip()
        
        if not url_value.startswith(('http://', 'https://')):
            raise ValidationError('URL must start with http:// or https://')
        
        # Check for valid domain structure
        if len(url_value.split('.')) < 2:
            raise ValidationError('Invalid URL format')


class UpdatePasswordForm(FlaskForm):
    """Form for changing password"""
    
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message='Current password is required')
    ])
    
    new_password = PasswordField('New Password', validators=[
        DataRequired(message='New password is required'),
        Length(min=8, message='Password must be at least 8 characters'),
        Regexp(
            r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)',
            message='Password must contain uppercase letter, lowercase letter, and number'
        )
    ])
    
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Password confirmation is required')
    ])
    
    submit = SubmitField('Update Password')
    
    def validate_confirm_password(self, field):
        """Check that password and confirm_password match"""
        if self.new_password.data != field.data:
            raise ValidationError('Passwords do not match')
