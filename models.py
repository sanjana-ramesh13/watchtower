from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """User model - stores information about app users"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to websites
    websites = db.relationship('Website', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and store password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches stored hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Website(db.Model):
    """Website model - stores websites to monitor"""
    __tablename__ = 'websites'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Website {self.name}>'


class MonitoringResult(db.Model):
    """Monitoring result - stores each website check"""
    __tablename__ = 'monitoring_results'
    
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(db.Integer, db.ForeignKey('websites.id'), nullable=False)
    status_code = db.Column(db.Integer, nullable=True)
    response_time_ms = db.Column(db.Float, nullable=True)
    is_up = db.Column(db.Boolean, nullable=False)
    error_message = db.Column(db.String(255), nullable=True)
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)
    alert_sent = db.Column(db.Boolean, default=False)
    
    # Relationship back to website
    website = db.relationship('Website', backref='monitoring_results')
    
    def __repr__(self):
        return f'<MonitoringResult {self.website_id} - {"UP" if self.is_up else "DOWN"}>'
