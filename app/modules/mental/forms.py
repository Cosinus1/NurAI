from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, IntegerField, BooleanField, 
    SubmitField, SelectField, DateField, DateTimeField
)
from wtforms.validators import DataRequired, Optional, NumberRange, Length
from flask_babel import lazy_gettext as _l

class MentalWellnessForm(FlaskForm):
    """Form for tracking daily mental wellness."""
    # Mood tracking (scale 1-10)
    mood_rating = IntegerField(_l('Current Mood (1-10)'), 
                               validators=[Optional(), NumberRange(min=1, max=10)],
                               description=_l('1 = Very Poor, 10 = Excellent'))
    
    anxiety_level = IntegerField(_l('Anxiety Level (1-10)'), 
                                validators=[Optional(), NumberRange(min=1, max=10)],
                                description=_l('1 = None, 10 = Severe'))
    
    depression_level = IntegerField(_l('Depression Level (1-10)'), 
                                   validators=[Optional(), NumberRange(min=1, max=10)],
                                   description=_l('1 = None, 10 = Severe'))
    
    # Emotional wellness
    focus_clarity = IntegerField(_l('Mental Focus/Clarity (1-10)'), 
                                validators=[Optional(), NumberRange(min=1, max=10)])
    
    motivation = IntegerField(_l('Motivation Level (1-10)'), 
                             validators=[Optional(), NumberRange(min=1, max=10)])
    
    social_connection = IntegerField(_l('Social Connection (1-10)'), 
                                    validators=[Optional(), NumberRange(min=1, max=10)],
                                    description=_l('How connected do you feel to others'))
    
    # Wellness activities
    meditation_minutes = IntegerField(_l('Meditation/Mindfulness (minutes)'), 
                                     validators=[Optional(), NumberRange(min=0)])
    
    gratitude_practice = BooleanField(_l('Practiced gratitude today'))
    
    therapy_session = BooleanField(_l('Had therapy session today'))
    
    # Stressors (multiple choice checkbox in UI)
    work_stress = BooleanField(_l('Work/Academic Stress'))
    financial_stress = BooleanField(_l('Financial Stress'))
    relationship_stress = BooleanField(_l('Relationship Stress'))
    health_stress = BooleanField(_l('Health-related Stress'))
    
    # Notes
    triggers = TextAreaField(_l('Triggers or Stressors Today'), validators=[Optional()])
    coping_strategies = TextAreaField(_l('Coping Strategies Used'), validators=[Optional()])
    journal_entry = TextAreaField(_l('Journal Entry'), validators=[Optional()])
    
    submit = SubmitField(_l('Save Entry'))

class MoodJournalForm(FlaskForm):
    """Form for mood journaling."""
    journal_entry = TextAreaField(_l('Journal Entry'), 
                                 validators=[DataRequired()],
                                 description=_l('Write about your feelings, thoughts, challenges, and victories today.'))
    
    submit = SubmitField(_l('Save Journal Entry'))

class TherapySessionForm(FlaskForm):
    """Form for recording therapy sessions."""
    date = DateTimeField(_l('Session Date & Time'), 
                        format='%Y-%m-%d %H:%M',
                        validators=[DataRequired()])
    
    therapist = StringField(_l('Therapist Name'), validators=[DataRequired()])
    
    session_type = SelectField(_l('Type of Therapy'), 
                              choices=[
                                  ('', _l('Select...')),
                                  ('cbt', _l('Cognitive Behavioral Therapy (CBT)')),
                                  ('psychodynamic', _l('Psychodynamic Therapy')),
                                  ('interpersonal', _l('Interpersonal Therapy')),
                                  ('humanistic', _l('Humanistic Therapy')),
                                  ('emdr', _l('EMDR')),
                                  ('group', _l('Group Therapy')),
                                  ('family', _l('Family Therapy')),
                                  ('other', _l('Other'))
                              ],
                              validators=[DataRequired()])
    
    notes = TextAreaField(_l('Session Notes'), 
                         validators=[Optional()],
                         description=_l('Key points discussed, insights, homework, etc.'))
    
    follow_up_date = DateField(_l('Next Session Date'), 
                              format='%Y-%m-%d',
                              validators=[Optional()])
    
    submit = SubmitField(_l('Record Session'))

class MentalWellnessFilterForm(FlaskForm):
    """Form for filtering mental wellness history."""
    start_date = DateField(_l('Start Date'), format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField(_l('End Date'), format='%Y-%m-%d', validators=[Optional()])
    
    submit = SubmitField(_l('Filter'))