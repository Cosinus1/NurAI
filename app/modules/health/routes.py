from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_babel import gettext as _

from app import db
from app.modules.health.models import HealthSurvey
from app.modules.health.forms import HealthSurveyForm, HealthSurveyFilterForm, MedicationForm

# Create blueprint
health_bp = Blueprint('health', __name__, url_prefix='/health')

@health_bp.route('/')
@login_required
def index():
    """Health tracking overview."""
    # Get recent health survey entries
    recent_entries = HealthSurvey.query.filter_by(user_id=current_user.id)\
        .order_by(HealthSurvey.date.desc())\
        .limit(7).all()
    
    # Calculate averages for key metrics (last 7 days)
    avg_data = {}
    if recent_entries:
        avg_data['sleep_duration'] = sum(entry.sleep_duration or 0 for entry in recent_entries) / len(recent_entries)
        avg_data['energy_level'] = sum(entry.energy_level or 0 for entry in recent_entries) / len(recent_entries)
        avg_data['stress_level'] = sum(entry.stress_level or 0 for entry in recent_entries) / len(recent_entries)
        avg_data['water_intake'] = sum(entry.water_intake or 0 for entry in recent_entries) / len(recent_entries)
    
    # Get last entry for vital signs
    last_entry = recent_entries[0] if recent_entries else None
    
    return render_template('health/index.html',
                           title=_('Health Tracking'),
                           recent_entries=recent_entries,
                           avg_data=avg_data,
                           last_entry=last_entry)

@health_bp.route('/track', methods=['GET', 'POST'])
@login_required
def track():
    """Form to track daily health metrics."""
    form = HealthSurveyForm()
    
    # Set default date to today
    if request.method == 'GET':
        form.date.data = datetime.utcnow().date()
    
    if form.validate_on_submit():
        # Check if an entry for this date already exists
        existing_entry = HealthSurvey.query.filter_by(
            user_id=current_user.id,
            date=form.date.data
        ).first()
        
        if existing_entry:
            # Update existing entry
            existing_entry.weight = form.weight.data
            existing_entry.blood_pressure_systolic = form.blood_pressure_systolic.data
            existing_entry.blood_pressure_diastolic = form.blood_pressure_diastolic.data
            existing_entry.heart_rate = form.heart_rate.data
            existing_entry.body_temperature = form.body_temperature.data
            existing_entry.sleep_duration = form.sleep_duration.data
            existing_entry.sleep_quality = form.sleep_quality.data
            existing_entry.energy_level = form.energy_level.data
            existing_entry.stress_level = form.stress_level.data
            existing_entry.water_intake = form.water_intake.data
            existing_entry.meal_quality = form.meal_quality.data
            existing_entry.alcohol_consumption = form.alcohol_consumption.data
            existing_entry.smoking = form.smoking.data
            existing_entry.symptoms = form.symptoms.data
            existing_entry.notes = form.notes.data
            
            flash(_('Health survey updated for the selected date.'), 'success')
        else:
            # Create new entry
            entry = HealthSurvey(
                user_id=current_user.id,
                date=form.date.data,
                weight=form.weight.data,
                blood_pressure_systolic=form.blood_pressure_systolic.data,
                blood_pressure_diastolic=form.blood_pressure_diastolic.data,
                heart_rate=form.heart_rate.data,
                body_temperature=form.body_temperature.data,
                sleep_duration=form.sleep_duration.data,
                sleep_quality=form.sleep_quality.data,
                energy_level=form.energy_level.data,
                stress_level=form.stress_level.data,
                water_intake=form.water_intake.data,
                meal_quality=form.meal_quality.data,
                alcohol_consumption=form.alcohol_consumption.data,
                smoking=form.smoking.data,
                symptoms=form.symptoms.data,
                notes=form.notes.data
            )
            db.session.add(entry)
            flash(_('Health survey recorded.'), 'success')
        
        db.session.commit()
        return redirect(url_for('health.index'))
    
    return render_template('health/track.html',
                           title=_('Track Health Metrics'),
                           form=form)

@health_bp.route('/history')
@login_required
def history():
    """View health survey history."""
    filter_form = HealthSurveyFilterForm()
    
    # Apply filters if provided
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    
    query = HealthSurvey.query.filter_by(user_id=current_user.id)
    
    if start_date:
        query = query.filter(HealthSurvey.date >= start_date)
    if end_date:
        query = query.filter(HealthSurvey.date <= end_date)
    
    entries = query.order_by(HealthSurvey.date.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('health/history.html',
                           title=_('Health Survey History'),
                           entries=entries,
                           filter_form=filter_form)

@health_bp.route('/medications', methods=['GET', 'POST'])
@login_required
def medications():
    """Medication tracking."""
    form = MedicationForm()
    
    if form.validate_on_submit():
        # In a real app, you would save to a Medication model
        # For this demo, we'll just show a success message
        flash(_('Medication saved successfully.'), 'success')
        return redirect(url_for('health.medications'))
    
    # In a real app, you would fetch medications from database
    medications = []
    
    return render_template('health/medications.html',
                           title=_('Medication Tracking'),
                           form=form,
                           medications=medications)

@health_bp.route('/delete_entry/<int:id>', methods=['POST'])
@login_required
def delete_entry(id):
    """Delete a health survey entry."""
    entry = HealthSurvey.query.get_or_404(id)
    
    # Check that user owns this entry
    if entry.user_id != current_user.id:
        flash(_('You do not have permission to delete this entry.'), 'danger')
        return redirect(url_for('health.history'))
    
    db.session.delete(entry)
    db.session.commit()
    flash(_('Health survey entry deleted.'), 'success')
    return redirect(url_for('health.history'))

@health_bp.route('/edit_entry/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
    """Edit a health survey entry."""
    entry = HealthSurvey.query.get_or_404(id)
    
    # Check that user owns this entry
    if entry.user_id != current_user.id:
        flash(_('You do not have permission to edit this entry.'), 'danger')
        return redirect(url_for('health.history'))
    
    form = HealthSurveyForm()
    
    if form.validate_on_submit():
        entry.date = form.date.data
        entry.weight = form.weight.data
        entry.blood_pressure_systolic = form.blood_pressure_systolic.data
        entry.blood_pressure_diastolic = form.blood_pressure_diastolic.data
        entry.heart_rate = form.heart_rate.data
        entry.body_temperature = form.body_temperature.data
        entry.sleep_duration = form.sleep_duration.data
        entry.sleep_quality = form.sleep_quality.data
        entry.energy_level = form.energy_level.data
        entry.stress_level = form.stress_level.data
        entry.water_intake = form.water_intake.data
        entry.meal_quality = form.meal_quality.data
        entry.alcohol_consumption = form.alcohol_consumption.data
        entry.smoking = form.smoking.data
        entry.symptoms = form.symptoms.data
        entry.notes = form.notes.data
        
        db.session.commit()
        flash(_('Health survey entry updated.'), 'success')
        return redirect(url_for('health.history'))
    
    # Pre-populate form with existing data
    elif request.method == 'GET':
        form.date.data = entry.date
        form.weight.data = entry.weight
        form.blood_pressure_systolic.data = entry.blood_pressure_systolic
        form.blood_pressure_diastolic.data = entry.blood_pressure_diastolic
        form.heart_rate.data = entry.heart_rate
        form.body_temperature.data = entry.body_temperature
        form.sleep_duration.data = entry.sleep_duration
        form.sleep_quality.data = entry.sleep_quality
        form.energy_level.data = entry.energy_level
        form.stress_level.data = entry.stress_level
        form.water_intake.data = entry.water_intake
        form.meal_quality.data = entry.meal_quality
        form.alcohol_consumption.data = entry.alcohol_consumption
        form.smoking.data = entry.smoking
        form.symptoms.data = entry.symptoms
        form.notes.data = entry.notes
    
    return render_template('health/edit_entry.html',
                           title=_('Edit Health Survey'),
                           form=form)