import os
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import SECRET_KEY, DEBUG, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db
from email_service import mail
from routes import register_routes
from scheduler import start_scheduler

# Create Flask app
app = Flask(__name__)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Load configuration
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# Override with environment variable if set (for Railway/Render)
db_url = os.environ.get('DATABASE_URL')
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sanjana.ramesh2413@gmail.com'
app.config['MAIL_PASSWORD'] = 'rvkz whic fwrz amuj'
app.config['MAIL_DEFAULT_SENDER'] = 'sanjana.ramesh2413@gmail.com'
app.config['SEND_ALERT_EMAILS'] = True

# Initialize database and mail
db.init_app(app)
mail.init_app(app)

# Register routes
register_routes(app)

# Start background scheduler for periodic checks
start_scheduler()

# Security headers
@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    
    # Prevent clickjacking attacks
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Enable XSS protection
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Referrer policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Permissions policy
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    return response

# Create database tables (if they don't exist)
with app.app_context():
    db.create_all()
    print("✅ Database initialized!")

if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
