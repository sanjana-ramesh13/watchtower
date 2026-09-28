import os

# Get DATABASE_URL from environment, ensure it uses psycopg2
db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres@localhost/watchtower')

# Convert postgresql:// to postgresql+psycopg2://
if db_url and 'postgresql://' in db_url and 'psycopg2' not in db_url:
    db_url = db_url.replace('postgresql://', 'postgresql+psycopg2://')

DATABASE_URL = db_url
SQLALCHEMY_DATABASE_URI = DATABASE_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'dev-key-change-in-production'
DEBUG = False

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'sanjana.ramesh2413@gmail.com'
MAIL_PASSWORD = 'rvkz whic fwrz amuj'
MAIL_DEFAULT_SENDER = 'sanjana.ramesh2413@gmail.com'
SEND_ALERT_EMAILS = True
