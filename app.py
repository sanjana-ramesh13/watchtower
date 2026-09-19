import os
from flask import Flask
from config import SECRET_KEY, DEBUG, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db
from email_service import mail
from routes import register_routes
from scheduler import start_scheduler

# Create Flask app
app = Flask(__name__)

# Load configuration
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# Override with environment variable if set (for Railway)
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

# Create database tables (if they don't exist)
with app.app_context():
    db.create_all()
    print("✅ Database initialized!")

if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
