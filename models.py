from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    websites = db.relationship('Website', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Website(db.Model):
    """Website model for monitoring"""
    __tablename__ = 'websites'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    results = db.relationship('MonitoringResult', backref='website', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Website {self.url}>'

class MonitoringResult(db.Model):
    """Monitoring result model for check history"""
    __tablename__ = 'monitoring_results'
    
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(db.Integer, db.ForeignKey('websites.id'), nullable=False)
    status_code = db.Column(db.Integer)
    response_time = db.Column(db.Float)
    is_up = db.Column(db.Boolean)
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)
    alert_sent = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<MonitoringResult {self.website_id} - {self.status_code}>'
