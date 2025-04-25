from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_babel import gettext as _

from app import db
from app.auth.models import User
from app.auth.forms import (
    LoginForm, RegistrationForm, ProfileForm, 
    ChangePasswordForm, RequestResetForm, ResetPasswordForm
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('core.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash(_('Registration successful! You can now log in.'), 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title=_('Register'), form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for('core.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Check if the user entered email or username
        if '@' in form.username.data:
            user = User.query.filter_by(email=form.username.data).first()
        else:
            user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'), 'danger')
            return redirect(url_for('auth.login'))
        
        # Update last login time
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Login the user
        login_user(user, remember=form.remember_me.data)
        
        # Set language preference from user profile
        if user.language_preference:
            session['language'] = user.language_preference
        
        # Redirect to the page the user was trying to access
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('core.dashboard')
        
        return redirect(next_page)
    
    return render_template('auth/login.html', title=_('Login'), form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash(_('You have been logged out.'), 'info')
    return redirect(url_for('core.index'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page."""
    form = ProfileForm()
    
    if request.method == 'GET':
        # Pre-populate form with current user data
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.date_of_birth.data = current_user.date_of_birth
        form.gender.data = current_user.gender
        form.height.data = current_user.height
        form.weight.data = current_user.weight
        form.language_preference.data = current_user.language_preference
    
    if form.validate_on_submit():
        # Check if email is being changed and is already in use
        if form.email.data != current_user.email:
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None:
                flash(_('Email already in use. Please choose a different one.'), 'danger')
                return redirect(url_for('auth.profile'))
        
        # Update user profile
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.date_of_birth = form.date_of_birth.data
        current_user.gender = form.gender.data
        current_user.height = form.height.data
        current_user.weight = form.weight.data
        
        # Update language preference
        if form.language_preference.data != current_user.language_preference:
            current_user.language_preference = form.language_preference.data
            session['language'] = form.language_preference.data
        
        db.session.commit()
        flash(_('Your profile has been updated.'), 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/profile.html', title=_('Profile'), form=form)

@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password page."""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash(_('Current password is incorrect.'), 'danger')
            return redirect(url_for('auth.change_password'))
        
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash(_('Your password has been updated.'), 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/change_password.html', title=_('Change Password'), form=form)

@auth_bp.route('/request_reset', methods=['GET', 'POST'])
def request_reset():
    """Request password reset page."""
    if current_user.is_authenticated:
        return redirect(url_for('core.dashboard'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # In a real application, you would send an email with reset link
            # For this demo, we'll just redirect to the reset page
            flash(_('Password reset instructions have been sent to your email.'), 'info')
            return redirect(url_for('auth.reset_password', token='demo_token'))
        else:
            flash(_('No account found with that email address.'), 'warning')
    
    return render_template('auth/request_reset.html', title=_('Reset Password'), form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password page."""
    if current_user.is_authenticated:
        return redirect(url_for('core.dashboard'))
    
    # In a real application, you would validate the token and get the user
    # For this demo, we'll just show the reset form
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Here you would find the user by token and set the new password
        flash(_('Your password has been reset. You can now log in.'), 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', title=_('Reset Password'), form=form)