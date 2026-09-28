import os
from flask import Flask
from config import SECRET_KEY, DEBUG, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db
from email_service import mail
from routes import register_routes
from scheduler import start_scheduler

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# Override with environment variable if set
db_url = os.environ.get('DATABASE_URL')
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sanjana.ramesh2413@gmail.com'
app.config['MAIL_PASSWORD'] = 'rvkz whic fwrz amuj'
app.config['MAIL_DEFAULT_SENDER'] = 'sanjana.ramesh2413@gmail.com'
app.config['SEND_ALERT_EMAILS'] = True

db.init_app(app)
mail.init_app(app)

register_routes(app)
start_scheduler()

with app.app_context():
    db.create_all()
    print("✅ Database initialized!")

if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
