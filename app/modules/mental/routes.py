from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_babel import gettext as _

from app import db
from app.modules.mental.models import MentalWellness, TherapySession
from app.modules.mental.forms import (
    MentalWellnessForm, TherapySessionForm, MoodJournalForm,
    MentalWellnessFilterForm
)

# Create blueprint
mental_bp = Blueprint('mental', __name__, url_prefix='/mental')

@mental_bp.route('/')
@login_required
def index():
    """Mental wellness tracking overview."""
    # Get recent mental wellness entries
    recent_entries = MentalWellness.query.filter_by(user_id=current_user.id)\
        .order_by(MentalWellness.date.desc())\
        .limit(7).all()
    
    # Get recent therapy sessions
    recent_sessions = TherapySession.query.filter_by(user_id=current_user.id)\
        .order_by(TherapySession.date.desc())\
        .limit(3).all()
    
    # Calculate mood average for the past week
    mood_avg = 0
    if recent_entries:
        mood_avg = sum(entry.mood_rating for entry in recent_entries) / len(recent_entries)
    
    return render_template('mental/index.html',
                           title=_('Mental Wellness'),
                           recent_entries=recent_entries,
                           recent_sessions=recent_sessions,
                           mood_avg=mood_avg)

@mental_bp.route('/track', methods=['GET', 'POST'])
@login_required
def track():
    """Form to track daily mental wellness."""
    form = MentalWellnessForm()
    
    if form.validate_on_submit():
        # Check if an entry for today already exists
        today = datetime.utcnow().date()
        existing_entry = MentalWellness.query.filter_by(
            user_id=current_user.id,
            date=today
        ).first()
        
        if existing_entry:
            # Update existing entry
            existing_entry.mood_rating = form.mood_rating.data
            existing_entry.anxiety_level = form.anxiety_level.data
            existing_entry.depression_level = form.depression_level.data
            existing_entry.focus_clarity = form.focus_clarity.data
            existing_entry.motivation = form.motivation.data
            existing_entry.social_connection = form.social_connection.data
            existing_entry.meditation_minutes = form.meditation_minutes.data
            existing_entry.gratitude_practice = form.gratitude_practice.data
            existing_entry.therapy_session = form.therapy_session.data
            existing_entry.work_stress = form.work_stress.data
            existing_entry.financial_stress = form.financial_stress.data
            existing_entry.relationship_stress = form.relationship_stress.data
            existing_entry.health_stress = form.health_stress.data
            existing_entry.triggers = form.triggers.data
            existing_entry.coping_strategies = form.coping_strategies.data
            existing_entry.journal_entry = form.journal_entry.data
            
            flash(_('Mental wellness entry updated for today.'), 'success')
        else:
            # Create new entry
            entry = MentalWellness(
                user_id=current_user.id,
                mood_rating=form.mood_rating.data,
                anxiety_level=form.anxiety_level.data,
                depression_level=form.depression_level.data,
                focus_clarity=form.focus_clarity.data,
                motivation=form.motivation.data,
                social_connection=form.social_connection.data,
                meditation_minutes=form.meditation_minutes.data,
                gratitude_practice=form.gratitude_practice.data,
                therapy_session=form.therapy_session.data,
                work_stress=form.work_stress.data,
                financial_stress=form.financial_stress.data,
                relationship_stress=form.relationship_stress.data,
                health_stress=form.health_stress.data,
                triggers=form.triggers.data,
                coping_strategies=form.coping_strategies.data,
                journal_entry=form.journal_entry.data
            )
            db.session.add(entry)
            flash(_('Mental wellness entry recorded.'), 'success')
        
        db.session.commit()
        return redirect(url_for('mental.index'))
    
    return render_template('mental/track.html',
                           title=_('Track Mental Wellness'),
                           form=form)

@mental_bp.route('/history')
@login_required
def history():
    """View mental wellness history."""
    filter_form = MentalWellnessFilterForm()
    
    # Apply filters if provided
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    
    query = MentalWellness.query.filter_by(user_id=current_user.id)
    
    if start_date:
        query = query.filter(MentalWellness.date >= start_date)
    if end_date:
        query = query.filter(MentalWellness.date <= end_date)
    
    entries = query.order_by(MentalWellness.date.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('mental/history.html',
                           title=_('Mental Wellness History'),
                           entries=entries,
                           filter_form=filter_form)

@mental_bp.route('/journal', methods=['GET', 'POST'])
@login_required
def journal():
    """Mental wellness journal."""
    form = MoodJournalForm()
    
    if form.validate_on_submit():
        # Check if an entry for today already exists
        today = datetime.utcnow().date()
        existing_entry = MentalWellness.query.filter_by(
            user_id=current_user.id,
            date=today
        ).first()
        
        if existing_entry:
            # Update existing entry with journal
            existing_entry.journal_entry = form.journal_entry.data
            flash(_('Journal entry updated for today.'), 'success')
        else:
            # Create new entry with just the journal
            entry = MentalWellness(
                user_id=current_user.id,
                journal_entry=form.journal_entry.data
            )
            db.session.add(entry)
            flash(_('Journal entry recorded.'), 'success')
        
        db.session.commit()
        return redirect(url_for('mental.journal'))
    
    # Get recent journal entries
    recent_journals = MentalWellness.query.filter_by(user_id=current_user.id)\
        .filter(MentalWellness.journal_entry.isnot(None))\
        .order_by(MentalWellness.date.desc())\
        .limit(10).all()
    
    return render_template('mental/journal.html',
                           title=_('Mood Journal'),
                           form=form,
                           recent_journals=recent_journals)

@mental_bp.route('/therapy', methods=['GET', 'POST'])
@login_required
def therapy():
    """Track therapy sessions."""
    form = TherapySessionForm()
    
    if form.validate_on_submit():
        session = TherapySession(
            user_id=current_user.id,
            date=form.date.data,
            therapist=form.therapist.data,
            session_type=form.session_type.data,
            notes=form.notes.data,
            follow_up_date=form.follow_up_date.data
        )
        db.session.add(session)
        db.session.commit()
        flash(_('Therapy session recorded.'), 'success')
        return redirect(url_for('mental.therapy'))
    
    # Get all therapy sessions
    sessions = TherapySession.query.filter_by(user_id=current_user.id)\
        .order_by(TherapySession.date.desc()).all()
    
    return render_template('mental/therapy.html',
                           title=_('Therapy Sessions'),
                           form=form,
                           sessions=sessions)

@mental_bp.route('/delete_entry/<int:id>', methods=['POST'])
@login_required
def delete_entry(id):
    """Delete a mental wellness entry."""
    entry = MentalWellness.query.get_or_404(id)
    
    # Check that user owns this entry
    if entry.user_id != current_user.id:
        flash(_('You do not have permission to delete this entry.'), 'danger')
        return redirect(url_for('mental.history'))
    
    db.session.delete(entry)
    db.session.commit()
    flash(_('Mental wellness entry deleted.'), 'success')
    return redirect(url_for('mental.history'))

@mental_bp.route('/edit_entry/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
    """Edit a mental wellness entry."""
    entry = MentalWellness.query.get_or_404(id)
    
    # Check that user owns this entry
    if entry.user_id != current_user.id:
        flash(_('You do not have permission to edit this entry.'), 'danger')
        return redirect(url_for('mental.history'))
    
    form = MentalWellnessForm()
    
    if form.validate_on_submit():
        entry.mood_rating = form.mood_rating.data
        entry.anxiety_level = form.anxiety_level.data
        entry.depression_level = form.depression_level.data
        entry.focus_clarity = form.focus_clarity.data
        entry.motivation = form.motivation.data
        entry.social_connection = form.social_connection.data
        entry.meditation_minutes = form.meditation_minutes.data
        entry.gratitude_practice = form.gratitude_practice.data
        entry.therapy_session = form.therapy_session.data
        entry.work_stress = form.work_stress.data
        entry.financial_stress = form.financial_stress.data
        entry.relationship_stress = form.relationship_stress.data
        entry.health_stress = form.health_stress.data
        entry.triggers = form.triggers.data
        entry.coping_strategies = form.coping_strategies.data
        entry.journal_entry = form.journal_entry.data
        
        db.session.commit()
        flash(_('Mental wellness entry updated.'), 'success')
        return redirect(url_for('mental.history'))
    
    # Pre-populate form with existing data
    elif request.method == 'GET':
        form.mood_rating.data = entry.mood_rating
        form.anxiety_level.data = entry.anxiety_level
        form.depression_level.data = entry.depression_level
        form.focus_clarity.data = entry.focus_clarity
        form.motivation.data = entry.motivation
        form.social_connection.data = entry.social_connection
        form.meditation_minutes.data = entry.meditation_minutes
        form.gratitude_practice.data = entry.gratitude_practice
        form.therapy_session.data = entry.therapy_session
        form.work_stress.data = entry.work_stress
        form.financial_stress.data = entry.financial_stress
        form.relationship_stress.data = entry.relationship_stress
        form.health_stress.data = entry.health_stress
        form.triggers.data = entry.triggers
        form.coping_strategies.data = entry.coping_strategies
        form.journal_entry.data = entry.journal_entry
    
    return render_template('mental/edit_entry.html',
                           title=_('Edit Mental Wellness Entry'),
                           form=form)