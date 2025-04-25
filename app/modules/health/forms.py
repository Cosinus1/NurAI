from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, IntegerField, FloatField, BooleanField, 
    SubmitField, SelectField, DateField
)
from wtforms.validators import DataRequired, Optional, NumberRange, Length
from flask_babel import lazy_gettext as _l

class HealthSurveyForm(FlaskForm):
    """Form for daily health tracking."""
    # Date
    date = DateField(_l('Date'), format='%Y-%m-%d', validators=[DataRequired()])
    
    # Vital signs
    weight = FloatField(_l('Weight (kg)'), validators=[Optional(), NumberRange(min=20, max=500)])
    
    blood_pressure_systolic = IntegerField(_l('Blood Pressure (Systolic)'), 
                                          validators=[Optional(), NumberRange(min=70, max=250)])
    
    blood_pressure_diastolic = IntegerField(_l('Blood Pressure (Diastolic)'), 
                                           validators=[Optional(), NumberRange(min=40, max=150)])
    
    heart_rate = IntegerField(_l('Heart Rate (bpm)'), 
                             validators=[Optional(), NumberRange(min=30, max=220)])
    
    body_temperature = FloatField(_l('Body Temperature (°C)'), 
                                 validators=[Optional(), NumberRange(min=35, max=42)])
    
    # Sleep metrics
    sleep_duration = FloatField(_l('Sleep Duration (hours)'), 
                               validators=[Optional(), NumberRange(min=0, max=24)])
    
    sleep_quality = IntegerField(_l('Sleep Quality (1-10)'), 
                                validators=[Optional(), NumberRange(min=1, max=10)],
                                description=_l('1 = Very Poor, 10 = Excellent'))
    
    # General health
    energy_level = IntegerField(_l('Energy Level (1-10)'), 
                               validators=[Optional(), NumberRange(min=1, max=10)],
                               description=_l('1 = Very Low, 10 = Very High'))
    
    stress_level = IntegerField(_l('Stress Level (1-10)'), 
                               validators=[Optional(), NumberRange(min=1, max=10)],
                               description=_l('1 = None, 10 = Extreme'))
    
    # Health habits
    water_intake = FloatField(_l('Water Intake (liters)'), 
                             validators=[Optional(), NumberRange(min=0, max=10)])
    
    meal_quality = IntegerField(_l('Meal Quality (1-10)'), 
                               validators=[Optional(), NumberRange(min=1, max=10)],
                               description=_l('1 = Very Poor, 10 = Excellent'))
    
    alcohol_consumption = BooleanField(_l('Consumed alcohol today'))
    
    smoking = BooleanField(_l('Smoked today'))
    
    # Notes
    symptoms = TextAreaField(_l('Any Symptoms'), validators=[Optional()],
                           description=_l('Describe any physical symptoms you experienced today'))
    
    notes = TextAreaField(_l('Additional Notes'), validators=[Optional()])
    
    submit = SubmitField(_l('Save Health Survey'))

class HealthSurveyFilterForm(FlaskForm):
    """Form for filtering health survey history."""
    start_date = DateField(_l('Start Date'), format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField(_l('End Date'), format='%Y-%m-%d', validators=[Optional()])
    
    submit = SubmitField(_l('Filter'))

class MedicationForm(FlaskForm):
    """Form for tracking medications."""
    name = StringField(_l('Medication Name'), validators=[DataRequired()])
    
    dosage = StringField(_l('Dosage'), validators=[DataRequired()])
    
    frequency = SelectField(_l('Frequency'), 
                           choices=[
                               ('', _l('Select...')),
                               ('once_daily', _l('Once daily')),
                               ('twice_daily', _l('Twice daily')),
                               ('three_times_daily', _l('Three times daily')),
                               ('four_times_daily', _l('Four times daily')),
                               ('as_needed', _l('As needed')),
                               ('other', _l('Other'))
                           ],
                           validators=[DataRequired()])
    
    start_date = DateField(_l('Start Date'), format='%Y-%m-%d', validators=[DataRequired()])
    
    end_date = DateField(_l('End Date'), format='%Y-%m-%d', validators=[Optional()],
                        description=_l('Leave blank if ongoing'))
    
    purpose = StringField(_l('Purpose'), validators=[Optional()])
    
    notes = TextAreaField(_l('Notes'), validators=[Optional()])
    
    submit = SubmitField(_l('Save Medication'))