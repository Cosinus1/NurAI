from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_login import login_required, current_user
from flask_babel import gettext as _

from app import db
from app.mental.models import MentalWellness
from app.health.models import HealthSurvey
from app.fitness.models import FitnessMetric

# Create blueprint
core_bp = Blueprint('core', __name__)

@core_bp.route('/')
def index():
    """Landing page."""
    if current_user.is_authenticated:
        return redirect(url_for('core.dashboard'))
    return render_template('index.html', title=_('Welcome to NurAI'))

@core_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with overview of all tracking modules."""
    # Get the most recent entries from each tracking module
    recent_mental = MentalWellness.query.filter_by(user_id=current_user.id).order_by(MentalWellness.date.desc()).first()
    recent_health = HealthSurvey.query.filter_by(user_id=current_user.id).order_by(HealthSurvey.date.desc()).first()
    recent_fitness = FitnessMetric.query.filter_by(user_id=current_user.id).order_by(FitnessMetric.date.desc()).first()
    
    # Get weekly statistics
    # In a real application, you would calculate averages, trends, etc.
    
    return render_template('dashboard.html', 
                          title=_('Dashboard'),
                          recent_mental=recent_mental,
                          recent_health=recent_health,
                          recent_fitness=recent_fitness)

@core_bp.route('/set_language/<language>')
def set_language(language):
    """Set the user interface language."""
    # Store the language preference in the session
    session['language'] = language
    
    # If user is logged in, store the preference in their profile
    if current_user.is_authenticated:
        current_user.language_preference = language
        db.session.commit()
    
    # Redirect back to the previous page or home
    next_page = request.args.get('next') or request.referrer or url_for('core.index')
    return redirect(next_page)

@core_bp.route('/about')
def about():
    """About page."""
    return render_template('about.html', title=_('About NurAI'))

@core_bp.route('/privacy')
def privacy():
    """Privacy policy page."""
    return render_template('privacy.html', title=_('Privacy Policy'))

@core_bp.route('/terms')
def terms():
    """Terms of service page."""
    return render_template('terms.html', title=_('Terms of Service'))

@core_bp.route('/help')
def help():
    """Help and FAQ page."""
    return render_template('help.html', title=_('Help & FAQ'))