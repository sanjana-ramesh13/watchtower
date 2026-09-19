import os

# Simple: just read DATABASE_URL if set, otherwise use default
DATABASE_URL = os.environ.get('DATABASE_URL') or 'postgresql://postgres@localhost/watchtower'

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
