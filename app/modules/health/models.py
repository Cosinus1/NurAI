from datetime import datetime
from app import db

class HealthSurvey(db.Model):
    """Model for general health survey data."""
    __tablename__ = 'health_surveys'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Vital signs
    weight = db.Column(db.Float)  # in kg
    blood_pressure_systolic = db.Column(db.Integer)
    blood_pressure_diastolic = db.Column(db.Integer)
    heart_rate = db.Column(db.Integer)  # bpm
    body_temperature = db.Column(db.Float)  # in °C
    
    # Sleep metrics
    sleep_duration = db.Column(db.Float)  # in hours
    sleep_quality = db.Column(db.Integer)  # scale 1-10
    
    # General health
    energy_level = db.Column(db.Integer)  # scale 1-10
    stress_level = db.Column(db.Integer)  # scale 1-10
    
    # Health habits
    water_intake = db.Column(db.Float)  # in liters
    meal_quality = db.Column(db.Integer)  # scale 1-10
    alcohol_consumption = db.Column(db.Boolean)
    smoking = db.Column(db.Boolean)
    
    # Notes
    symptoms = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<HealthSurvey {self.user_id} on {self.date}>'