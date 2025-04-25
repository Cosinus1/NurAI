from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, IntegerField, FloatField, BooleanField, 
    SubmitField, SelectField, DateField, FieldList, FormField
)
from wtforms.validators import DataRequired, Optional, NumberRange, Length
from flask_babel import lazy_gettext as _l

class FitnessMetricForm(FlaskForm):
    """Form for tracking fitness activities and metrics."""
    # Date
    date = DateField(_l('Date'), format='%Y-%m-%d', validators=[DataRequired()])
    
    # Activity metrics
    steps = IntegerField(_l('Steps'), validators=[Optional(), NumberRange(min=0)])
    
    distance = FloatField(_l('Distance (km)'), 
                         validators=[Optional(), NumberRange(min=0)])
    
    active_minutes = IntegerField(_l('Active Minutes'), 
                                 validators=[Optional(), NumberRange(min=0)])
    
    calories_burned = IntegerField(_l('Calories Burned'), 
                                  validators=[Optional(), NumberRange(min=0)])
    
    # Workout specific
    workout_type = SelectField(_l('Workout Type'), 
                              choices=[
                                  ('', _l('Select...')),
                                  ('running', _l('Running')),
                                  ('walking', _l('Walking')),
                                  ('cycling', _l('Cycling')),
                                  ('swimming', _l('Swimming')),
                                  ('strength', _l('Strength Training')),
                                  ('hiit', _l('HIIT')),
                                  ('yoga', _l('Yoga')),
                                  ('pilates', _l('Pilates')),
                                  ('other', _l('Other'))
                              ],
                              validators=[Optional()])
    
    workout_duration = IntegerField(_l('Workout Duration (minutes)'), 
                                   validators=[Optional(), NumberRange(min=0)])
    
    workout_intensity = IntegerField(_l('Workout Intensity (1-10)'), 
                                    validators=[Optional(), NumberRange(min=1, max=10)])
    
    # Performance metrics
    heart_rate_avg = IntegerField(_l('Average Heart Rate (bpm)'), 
                                 validators=[Optional(), NumberRange(min=30, max=220)])
    
    heart_rate_max = IntegerField(_l('Maximum Heart Rate (bpm)'), 
                                 validators=[Optional(), NumberRange(min=30, max=220)])
    
    # Recovery metrics
    recovery_score = IntegerField(_l('Recovery Score (1-10)'), 
                                 validators=[Optional(), NumberRange(min=1, max=10)],
                                 description=_l('1 = Poor, 10 = Excellent'))
    
    soreness_level = IntegerField(_l('Muscle Soreness (1-10)'), 
                                 validators=[Optional(), NumberRange(min=1, max=10)],
                                 description=_l('1 = None, 10 = Severe'))
    
    # Notes
    workout_notes = TextAreaField(_l('Workout Notes'), validators=[Optional()])
    
    submit = SubmitField(_l('Save Fitness Entry'))

class ExerciseEntryForm(FlaskForm):
    """Form for individual exercise within a workout."""
    name = StringField(_l('Exercise Name'), validators=[DataRequired()])
    sets = IntegerField(_l('Sets'), validators=[Optional(), NumberRange(min=0)])
    reps = IntegerField(_l('Reps'), validators=[Optional(), NumberRange(min=0)])
    weight = FloatField(_l('Weight (kg)'), validators=[Optional(), NumberRange(min=0)])
    duration = IntegerField(_l('Duration (seconds)'), validators=[Optional(), NumberRange(min=0)])
    notes = StringField(_l('Notes'), validators=[Optional()])

class WorkoutSessionForm(FlaskForm):
    """Form for tracking a complete workout session with exercises."""
    date = DateField(_l('Workout Date'), format='%Y-%m-%d', validators=[DataRequired()])
    
    workout_type = SelectField(_l('Workout Type'), 
                              choices=[
                                  ('', _l('Select...')),
                                  ('strength', _l('Strength Training')),
                                  ('cardio', _l('Cardio')),
                                  ('hiit', _l('HIIT')),
                                  ('flexibility', _l('Flexibility')),
                                  ('sport', _l('Sport')),
                                  ('mixed', _l('Mixed')),
                                  ('other', _l('Other'))
                              ],
                              validators=[DataRequired()])
    
    duration = IntegerField(_l('Total Duration (minutes)'), 
                           validators=[DataRequired(), NumberRange(min=1)])
    
    intensity = IntegerField(_l('Intensity (1-10)'), 
                            validators=[DataRequired(), NumberRange(min=1, max=10)])
    
    notes = TextAreaField(_l('Session Notes'), validators=[Optional()])
    
    # In a real application, you would use FieldList and FormField for exercises
    # For simplicity, we'll use separate fields for a few exercises
    exercise1_name = StringField(_l('Exercise 1'))
    exercise1_sets = IntegerField(_l('Sets'), validators=[Optional(), NumberRange(min=0)])
    exercise1_reps = IntegerField(_l('Reps'), validators=[Optional(), NumberRange(min=0)])
    exercise1_weight = FloatField(_l('Weight (kg)'), validators=[Optional(), NumberRange(min=0)])
    
    exercise2_name = StringField(_l('Exercise 2'))
    exercise2_sets = IntegerField(_l('Sets'), validators=[Optional(), NumberRange(min=0)])
    exercise2_reps = IntegerField(_l('Reps'), validators=[Optional(), NumberRange(min=0)])
    exercise2_weight = FloatField(_l('Weight (kg)'), validators=[Optional(), NumberRange(min=0)])
    
    exercise3_name = StringField(_l('Exercise 3'))
    exercise3_sets = IntegerField(_l('Sets'), validators=[Optional(), NumberRange(min=0)])
    exercise3_reps = IntegerField(_l('Reps'), validators=[Optional(), NumberRange(min=0)])
    exercise3_weight = FloatField(_l('Weight (kg)'), validators=[Optional(), NumberRange(min=0)])
    
    submit = SubmitField(_l('Save Workout'))

class WorkoutPlanForm(FlaskForm):
    """Form for creating a workout plan."""
    name = StringField(_l('Plan Name'), validators=[DataRequired()])
    description = TextAreaField(_l('Description'), validators=[Optional()])
    
    # In a real application, you would use nested forms for each day's workout
    # For simplicity, we'll use separate fields
    monday_type = SelectField(_l('Monday Workout'), 
                             choices=[
                                 ('', _l('Rest Day')),
                                 ('strength', _l('Strength Training')),
                                 ('cardio', _l('Cardio')),
                                 ('hiit', _l('HIIT')),
                                 ('flexibility', _l('Flexibility')),
                                 ('sport', _l('Sport')),
                                 ('mixed', _l('Mixed'))
                             ],
                             validators=[Optional()])
    
    tuesday_type = SelectField(_l('Tuesday Workout'), 
                              choices=[
                                  ('', _l('Rest Day')),
                                  ('strength', _l('Strength Training')),
                                  ('cardio', _l('Cardio')),
                                  ('hiit', _l('HIIT')),
                                  ('flexibility', _l('Flexibility')),
                                  ('sport', _l('Sport')),
                                  ('mixed', _l('Mixed'))
                              ],
                              validators=[Optional()])
    
    wednesday_type = SelectField(_l('Wednesday Workout'), 
                                choices=[
                                    ('', _l('Rest Day')),
                                    ('strength', _l('Strength Training')),
                                    ('cardio', _l('Cardio')),
                                    ('hiit', _l('HIIT')),
                                    ('flexibility', _l('Flexibility')),
                                    ('sport', _l('Sport')),
                                    ('mixed', _l('Mixed'))
                                ],
                                validators=[Optional()])
    
    thursday_type = SelectField(_l('Thursday Workout'), 
                               choices=[
                                   ('', _l('Rest Day')),
                                   ('strength', _l('Strength Training')),
                                   ('cardio', _l('Cardio')),
                                   ('hiit', _l('HIIT')),
                                   ('flexibility', _l('Flexibility')),
                                   ('sport', _l('Sport')),
                                   ('mixed', _l('Mixed'))
                               ],
                               validators=[Optional()])
    
    friday_type = SelectField(_l('Friday Workout'), 
                             choices=[
                                 ('', _l('Rest Day')),
                                 ('strength', _l('Strength Training')),
                                 ('cardio', _l('Cardio')),
                                 ('hiit', _l('HIIT')),
                                 ('flexibility', _l('Flexibility')),
                                 ('sport', _l('Sport')),
                                 ('mixed', _l('Mixed'))
                             ],
                             validators=[Optional()])
    
    saturday_type = SelectField(_l('Saturday Workout'), 
                               choices=[
                                   ('', _l('Rest Day')),
                                   ('strength', _l('Strength Training')),
                                   ('cardio', _l('Cardio')),
                                   ('hiit', _l('HIIT')),
                                   ('flexibility', _l('Flexibility')),
                                   ('sport', _l('Sport')),
                                   ('mixed', _l('Mixed'))
                               ],
                               validators=[Optional()])
    
    sunday_type = SelectField(_l('Sunday Workout'), 
                             choices=[
                                 ('', _l('Rest Day')),
                                 ('strength', _l('Strength Training')),
                                 ('cardio', _l('Cardio')),
                                 ('hiit', _l('HIIT')),
                                 ('flexibility', _l('Flexibility')),
                                 ('sport', _l('Sport')),
                                 ('mixed', _l('Mixed'))
                             ],
                             validators=[Optional()])
    
    submit = SubmitField(_l('Save Workout Plan'))

class FitnessFilterForm(FlaskForm):
    """Form for filtering fitness history."""
    start_date = DateField(_l('Start Date'), format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField(_l('End Date'), format='%Y-%m-%d', validators=[Optional()])
    workout_type = SelectField(_l('Workout Type'), 
                              choices=[
                                  ('', _l('All Types')),
                                  ('running', _l('Running')),
                                  ('walking', _l('Walking')),
                                  ('cycling', _l('Cycling')),
                                  ('swimming', _l('Swimming')),
                                  ('strength', _l('Strength Training')),
                                  ('hiit', _l('HIIT')),
                                  ('yoga', _l('Yoga')),
                                  ('pilates', _l('Pilates')),
                                  ('other', _l('Other'))
                              ],
                              validators=[Optional()])
    
    submit = SubmitField(_l('Filter'))