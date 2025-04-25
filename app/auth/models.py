from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):
    """User model for authentication and profile information."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    
    # Profile information
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(20))
    height = db.Column(db.Float)  # in cm
    weight = db.Column(db.Float)  # in kg
    
    # Preferences
    language_preference = db.Column(db.String(5), default='en')
    
    # Meta information
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    health_surveys = db.relationship('HealthSurvey', backref='user', lazy='dynamic')
    mental_wellness = db.relationship('MentalWellness', backref='user', lazy='dynamic')
    fitness_metrics = db.relationship('FitnessMetric', backref='user', lazy='dynamic')
    
    def __init__(self, username, email, password, **kwargs):
        super(User, self).__init__(**kwargs)
        self.username = username
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    """User loader for Flask-Login."""
    return User.query.get(int(user_id))