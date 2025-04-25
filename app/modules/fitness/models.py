from datetime import datetime
from app import db

class FitnessMetric(db.Model):
    """Model for fitness tracking."""
    __tablename__ = 'fitness_metrics'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Activity metrics
    steps = db.Column(db.Integer)
    distance = db.Column(db.Float)  # in km
    active_minutes = db.Column(db.Integer)
    calories_burned = db.Column(db.Integer)
    
    # Workout specific
    workout_type = db.Column(db.String(50))  # e.g., Running, Cycling, Strength, etc.
    workout_duration = db.Column(db.Integer)  # in minutes
    workout_intensity = db.Column(db.Integer)  # scale 1-10
    
    # Performance metrics
    heart_rate_avg = db.Column(db.Integer)
    heart_rate_max = db.Column(db.Integer)
    
    # Recovery metrics
    recovery_score = db.Column(db.Integer)  # scale 1-10
    soreness_level = db.Column(db.Integer)  # scale 1-10
    
    # Notes
    workout_notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<FitnessMetric {self.user_id} on {self.date} - {self.workout_type}>'

class WorkoutPlan(db.Model):
    """Model for workout plans."""
    __tablename__ = 'workout_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Workouts in this plan
    workouts = db.relationship('PlannedWorkout', backref='plan', lazy='dynamic')
    
    def __repr__(self):
        return f'<WorkoutPlan {self.name}>'

class PlannedWorkout(db.Model):
    """Model for individual workouts within a plan."""
    __tablename__ = 'planned_workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('workout_plans.id'), nullable=False)
    day_of_week = db.Column(db.Integer)  # 0=Monday, 6=Sunday
    workout_type = db.Column(db.String(50))
    duration = db.Column(db.Integer)  # in minutes
    description = db.Column(db.Text)
    
    # Exercises in this workout
    exercises = db.relationship('Exercise', backref='workout', lazy='dynamic')
    
    def __repr__(self):
        return f'<PlannedWorkout {self.workout_type} - Day {self.day_of_week}>'

class Exercise(db.Model):
    """Model for exercises within a workout."""
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('planned_workouts.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Float)  # in kg
    duration = db.Column(db.Integer)  # in seconds, for timed exercises
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Exercise {self.name} - {self.sets}x{self.reps}>'