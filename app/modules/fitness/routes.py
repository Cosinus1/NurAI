from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_babel import gettext as _

from app import db
from app.fitness.models import FitnessMetric, WorkoutPlan, PlannedWorkout, Exercise
from app.fitness.forms import (
    FitnessMetricForm, WorkoutSessionForm, WorkoutPlanForm, FitnessFilterForm
)

# Create blueprint
fitness_bp = Blueprint('fitness', __name__, url_prefix='/fitness')

@fitness_bp.route('/')
@login_required
def index():
    """Fitness tracking overview."""
    # Get recent fitness entries
    recent_entries = FitnessMetric.query.filter_by(user_id=current_user.id)\
        .order_by(FitnessMetric.date.desc())\
        .limit(7).all()
    
    # Calculate weekly totals
    week_start = datetime.utcnow().date() - timedelta(days=datetime.utcnow().weekday())
    week_end = week_start + timedelta(days=6)
    
    weekly_workouts = FitnessMetric.query.filter_by(user_id=current_user.id)\
        .filter(FitnessMetric.date >= week_start, FitnessMetric.date <= week_end)\
        .all()
    
    weekly_stats = {
        'total_workouts': len(weekly_workouts),
        'total_duration': sum(w.workout_duration or 0 for w in weekly_workouts),
        'total_distance': sum(w.distance or 0 for w in weekly_workouts),
        'total_calories': sum(w.calories_burned or 0 for w in weekly_workouts),
        'total_steps': sum(w.steps or 0 for w in weekly_workouts)
    }
    
    # Get active workout plan
    workout_plan = WorkoutPlan.query.filter_by(user_id=current_user.id).first()
    
    return render_template('fitness/index.html',
                           title=_('Fitness History'),
                           entries=entries,
                           filter_form=filter_form)

@fitness_bp.route('/workout_session', methods=['GET', 'POST'])
@login_required
def workout_session():
    """Track a complete workout session with exercises."""
    form = WorkoutSessionForm()
    
    # Set default date to today
    if request.method == 'GET':
        form.date.data = datetime.utcnow().date()
    
    if form.validate_on_submit():
        # First, create the fitness metric entry
        metric = FitnessMetric(
            user_id=current_user.id,
            date=form.date.data,
            workout_type=form.workout_type.data,
            workout_duration=form.duration.data,
            workout_intensity=form.intensity.data,
            workout_notes=form.notes.data
        )
        db.session.add(metric)
        
        # In a real application, you would also create Exercise entries
        # linked to this workout session
        
        db.session.commit()
        flash(_('Workout session recorded.'), 'success')
        return redirect(url_for('fitness.index'))
    
    return render_template('fitness/workout_session.html',
                           title=_('Track Workout Session'),
                           form=form)

@fitness_bp.route('/workout_plan', methods=['GET', 'POST'])
@login_required
def workout_plan():
    """Create or update workout plan."""
    form = WorkoutPlanForm()
    
    # Get existing plan if any
    existing_plan = WorkoutPlan.query.filter_by(user_id=current_user.id).first()
    
    if form.validate_on_submit():
        if existing_plan:
            # Update existing plan
            existing_plan.name = form.name.data
            existing_plan.description = form.description.data
            
            # In a real application, you would update the planned workouts
            # for each day of the week
            
            flash(_('Workout plan updated.'), 'success')
        else:
            # Create new plan
            plan = WorkoutPlan(
                user_id=current_user.id,
                name=form.name.data,
                description=form.description.data
            )
            db.session.add(plan)
            
            # In a real application, you would create PlannedWorkout entries
            # for each day of the week
            
            flash(_('Workout plan created.'), 'success')
        
        db.session.commit()
        return redirect(url_for('fitness.workout_plan'))
    
    # Pre-populate form with existing data
    elif request.method == 'GET' and existing_plan:
        form.name.data = existing_plan.name
        form.description.data = existing_plan.description
        
        # In a real application, you would also populate the workout types
        # for each day based on the existing planned workouts
    
    return render_template('fitness/workout_plan.html',
                           title=_('Workout Plan'),
                           form=form,
                           existing_plan=existing_plan)

@fitness_bp.route('/delete_entry/<int:id>', methods=['POST'])
@login_required
def delete_entry(id):
    """Delete a fitness metric entry."""
    entry = FitnessMetric.query.get_or_404(id)
    
    # Check that user owns this entry
    if entry.user_id != current_user.id:
        flash(_('You do not have permission to delete this entry.'), 'danger')
        return redirect(url_for('fitness.history'))
    
    db.session.delete(entry)
    db.session.commit()
    flash(_('Fitness entry deleted.'), 'success')
    return redirect(url_for('fitness.history'))

@fitness_bp.route('/edit_entry/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
    """Edit a fitness metric entry."""
    entry = FitnessMetric.query.get_or_404(id)
    
    # Check that user owns this entry
    if entry.user_id != current_user.id:
        flash(_('You do not have permission to edit this entry.'), 'danger')
        return redirect(url_for('fitness.history'))
    
    form = FitnessMetricForm()
    
    if form.validate_on_submit():
        entry.date = form.date.data
        entry.steps = form.steps.data
        entry.distance = form.distance.data
        entry.active_minutes = form.active_minutes.data
        entry.calories_burned = form.calories_burned.data
        entry.workout_type = form.workout_type.data
        entry.workout_duration = form.workout_duration.data
        entry.workout_intensity = form.workout_intensity.data
        entry.heart_rate_avg = form.heart_rate_avg.data
        entry.heart_rate_max = form.heart_rate_max.data
        entry.recovery_score = form.recovery_score.data
        entry.soreness_level = form.soreness_level.data
        entry.workout_notes = form.workout_notes.data
        
        db.session.commit()
        flash(_('Fitness entry updated.'), 'success')
        return redirect(url_for('fitness.history'))
    
    # Pre-populate form with existing data
    elif request.method == 'GET':
        form.date.data = entry.date
        form.steps.data = entry.steps
        form.distance.data = entry.distance
        form.active_minutes.data = entry.active_minutes
        form.calories_burned.data = entry.calories_burned
        form.workout_type.data = entry.workout_type
        form.workout_duration.data = entry.workout_duration
        form.workout_intensity.data = entry.workout_intensity
        form.heart_rate_avg.data = entry.heart_rate_avg
        form.heart_rate_max.data = entry.heart_rate_max
        form.recovery_score.data = entry.recovery_score
        form.soreness_level.data = entry.soreness_level
        form.workout_notes.data = entry.workout_notes
    
    return render_template('fitness/edit_entry.html',
                           title=_('Edit Fitness Entry'),
                           form=form)

@fitness_bp.route('/analytics')
@login_required
def analytics():
    """Fitness analytics and progress tracking."""
    # Get data for the past 30 days
    thirty_days_ago = datetime.utcnow().date() - timedelta(days=30)
    
    # Get workout counts by type
    workouts_by_type = db.session.query(
        FitnessMetric.workout_type, 
        db.func.count(FitnessMetric.id)
    ).filter(
        FitnessMetric.user_id == current_user.id,
        FitnessMetric.date >= thirty_days_ago,
        FitnessMetric.workout_type.isnot(None)
    ).group_by(
        FitnessMetric.workout_type
    ).all()
    
    # Get weekly workout minutes
    current_week_start = datetime.utcnow().date() - timedelta(days=datetime.utcnow().weekday())
    prev_week_start = current_week_start - timedelta(days=7)
    
    current_week_minutes = db.session.query(
        db.func.sum(FitnessMetric.workout_duration)
    ).filter(
        FitnessMetric.user_id == current_user.id,
        FitnessMetric.date >= current_week_start,
        FitnessMetric.workout_duration.isnot(None)
    ).scalar() or 0
    
    prev_week_minutes = db.session.query(
        db.func.sum(FitnessMetric.workout_duration)
    ).filter(
        FitnessMetric.user_id == current_user.id,
        FitnessMetric.date >= prev_week_start,
        FitnessMetric.date < current_week_start,
        FitnessMetric.workout_duration.isnot(None)
    ).scalar() or 0
    
    # Get daily activity data for charting
    daily_activities = FitnessMetric.query.filter(
        FitnessMetric.user_id == current_user.id,
        FitnessMetric.date >= thirty_days_ago
    ).order_by(FitnessMetric.date.asc()).all()
    
    return render_template('fitness/analytics.html',
                           title=_('Fitness Analytics'),
                           workouts_by_type=workouts_by_type,
                           current_week_minutes=current_week_minutes,
                           prev_week_minutes=prev_week_minutes,
                           daily_activities=daily_activities) Tracking'),
                           recent_entries=recent_entries,
                           weekly_stats=weekly_stats,
                           workout_plan=workout_plan)

@fitness_bp.route('/track', methods=['GET', 'POST'])
@login_required
def track():
    """Form to track fitness metrics."""
    form = FitnessMetricForm()
    
    # Set default date to today
    if request.method == 'GET':
        form.date.data = datetime.utcnow().date()
    
    if form.validate_on_submit():
        # Check if an entry for this date already exists
        existing_entry = FitnessMetric.query.filter_by(
            user_id=current_user.id,
            date=form.date.data
        ).first()
        
        if existing_entry:
            # Update existing entry
            existing_entry.steps = form.steps.data
            existing_entry.distance = form.distance.data
            existing_entry.active_minutes = form.active_minutes.data
            existing_entry.calories_burned = form.calories_burned.data
            existing_entry.workout_type = form.workout_type.data
            existing_entry.workout_duration = form.workout_duration.data
            existing_entry.workout_intensity = form.workout_intensity.data
            existing_entry.heart_rate_avg = form.heart_rate_avg.data
            existing_entry.heart_rate_max = form.heart_rate_max.data
            existing_entry.recovery_score = form.recovery_score.data
            existing_entry.soreness_level = form.soreness_level.data
            existing_entry.workout_notes = form.workout_notes.data
            
            flash(_('Fitness entry updated for the selected date.'), 'success')
        else:
            # Create new entry
            entry = FitnessMetric(
                user_id=current_user.id,
                date=form.date.data,
                steps=form.steps.data,
                distance=form.distance.data,
                active_minutes=form.active_minutes.data,
                calories_burned=form.calories_burned.data,
                workout_type=form.workout_type.data,
                workout_duration=form.workout_duration.data,
                workout_intensity=form.workout_intensity.data,
                heart_rate_avg=form.heart_rate_avg.data,
                heart_rate_max=form.heart_rate_max.data,
                recovery_score=form.recovery_score.data,
                soreness_level=form.soreness_level.data,
                workout_notes=form.workout_notes.data
            )
            db.session.add(entry)
            flash(_('Fitness entry recorded.'), 'success')
        
        db.session.commit()
        return redirect(url_for('fitness.index'))
    
    return render_template('fitness/track.html',
                           title=_('Track Fitness Metrics'),
                           form=form)

@fitness_bp.route('/history')
@login_required
def history():
    """View fitness history."""
    filter_form = FitnessFilterForm()
    
    # Apply filters if provided
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    workout_type = request.args.get('workout_type', None)
    
    query = FitnessMetric.query.filter_by(user_id=current_user.id)
    
    if start_date:
        query = query.filter(FitnessMetric.date >= start_date)
    if end_date:
        query = query.filter(FitnessMetric.date <= end_date)
    if workout_type:
        query = query.filter(FitnessMetric.workout_type == workout_type)
    
    entries = query.order_by(FitnessMetric.date.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('fitness/history.html',
                           title=_('Fitness