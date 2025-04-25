from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from flask_babel import lazy_gettext as _l

from app.auth.models import User

class LoginForm(FlaskForm):
    """User login form."""
    username = StringField(_l('Username or Email'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Log In'))

class RegistrationForm(FlaskForm):
    """User registration form."""
    username = StringField(_l('Username'), validators=[
        DataRequired(),
        Length(min=3, max=64)
    ])
    email = StringField(_l('Email'), validators=[
        DataRequired(),
        Email(),
        Length(max=120)
    ])
    password = PasswordField(_l('Password'), validators=[
        DataRequired(),
        Length(min=8)
    ])
    confirm_password = PasswordField(_l('Confirm Password'), validators=[
        DataRequired(),
        EqualTo('password', message=_l('Passwords must match'))
    ])
    submit = SubmitField(_l('Register'))
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('Username already in use. Please choose a different one.'))
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('Email already registered. Please use a different one.'))

class ProfileForm(FlaskForm):
    """User profile form."""
    first_name = StringField(_l('First Name'), validators=[Length(max=64)])
    last_name = StringField(_l('Last Name'), validators=[Length(max=64)])
    email = StringField(_l('Email'), validators=[DataRequired(), Email(), Length(max=120)])
    date_of_birth = DateField(_l('Date of Birth'), format='%Y-%m-%d', validators=[Optional()])
    gender = SelectField(_l('Gender'), choices=[
        ('', _l('Select...')),
        ('male', _l('Male')),
        ('female', _l('Female')),
        ('non-binary', _l('Non-binary')),
        ('other', _l('Other')),
        ('prefer_not_to_say', _l('Prefer not to say'))
    ], validators=[Optional()])
    height = FloatField(_l('Height (cm)'), validators=[Optional()])
    weight = FloatField(_l('Weight (kg)'), validators=[Optional()])
    language_preference = SelectField(_l('Language Preference'), choices=[
        ('en', _l('English')),
        ('fr', _l('French'))
    ])
    submit = SubmitField(_l('Update Profile'))

class ChangePasswordForm(FlaskForm):
    """Form for changing password."""
    current_password = PasswordField(_l('Current Password'), validators=[DataRequired()])
    new_password = PasswordField(_l('New Password'), validators=[
        DataRequired(),
        Length(min=8)
    ])
    confirm_new_password = PasswordField(_l('Confirm New Password'), validators=[
        DataRequired(),
        EqualTo('new_password', message=_l('Passwords must match'))
    ])
    submit = SubmitField(_l('Change Password'))

class RequestResetForm(FlaskForm):
    """Form for requesting password reset."""
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))

class ResetPasswordForm(FlaskForm):
    """Form for resetting password."""
    password = PasswordField(_l('New Password'), validators=[
        DataRequired(),
        Length(min=8)
    ])
    confirm_password = PasswordField(_l('Confirm Password'), validators=[
        DataRequired(),
        EqualTo('password', message=_l('Passwords must match'))
    ])
    submit = SubmitField(_l('Reset Password'))