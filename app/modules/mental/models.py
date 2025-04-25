from datetime import datetime
from app import db

class MentalWellness(db.Model):
    """Model for mental wellness tracking."""
    __tablename__ = 'mental_wellness'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Mood tracking (scale 1-10)
    mood_rating = db.Column(db.Integer)
    anxiety_level = db.Column(db.Integer)
    depression_level = db.Column(db.Integer)
    
    # Emotional wellness
    focus_clarity = db.Column(db.Integer)  # scale 1-10
    motivation = db.Column(db.Integer)  # scale 1-10
    social_connection = db.Column(db.Integer)  # scale 1-10
    
    # Wellness activities
    meditation_minutes = db.Column(db.Integer)
    gratitude_practice = db.Column(db.Boolean)
    therapy_session = db.Column(db.Boolean)
    
    # Stressors (multiple choice checkbox in UI)
    work_stress = db.Column(db.Boolean)
    financial_stress = db.Column(db.Boolean)
    relationship_stress = db.Column(db.Boolean)
    health_stress = db.Column(db.Boolean)
    
    # Notes
    triggers = db.Column(db.Text)
    coping_strategies = db.Column(db.Text)
    journal_entry = db.Column(db.Text)
    
    def __repr__(self):
        return f'<MentalWellness {self.user_id} on {self.date} - Mood: {self.mood_rating}>'
        
class TherapySession(db.Model):
    """Model for recording therapy sessions."""
    __tablename__ = 'therapy_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    therapist = db.Column(db.String(100))
    session_type = db.Column(db.String(50))  # CBT, Psychoanalysis, etc.
    notes = db.Column(db.Text)
    follow_up_date = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TherapySession {self.user_id} on {self.date.strftime("%Y-%m-%d")}>'