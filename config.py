# Configuration for WatchTower

# Database configuration
DATABASE_URL = 'postgresql://postgres@localhost/watchtower'

# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URI = DATABASE_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask configuration
SECRET_KEY = 'dev-key-change-in-production'
DEBUG = True

# Email configuration (Gmail)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'sanjana.ramesh2413@gmail.com'  # Change this to your Gmail
MAIL_PASSWORD = 'rvkz whic fwrz amuj'      # Change this to App Password
MAIL_DEFAULT_SENDER = 'sanjana.ramesh2413@gmail.com'

# Alert configuration
SEND_ALERT_EMAILS = True  # Can disable for testing# Configuration for WatchTower

# Database configuration
DATABASE_URL = 'postgresql://postgres@localhost/watchtower'
# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URI = DATABASE_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask configuration
SECRET_KEY = 'dev-key-change-in-production'
DEBUG = True
