from flask import Flask, request, session, g, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel

from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
babel = Babel()

def create_app(config_name='default'):
    """Application factory for Flask app."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    babel.init_app(app)

    # Configure login behavior
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.core.routes import core_bp
    app.register_blueprint(core_bp)

    from app.modules.health.routes import health_bp
    app.register_blueprint(health_bp)

    from app.modules.mental.routes import mental_bp
    app.register_blueprint(mental_bp)

    from app.modules.fitness.routes import fitness_bp
    app.register_blueprint(fitness_bp)

    # Configure language handling
    @babel.locale_selector
    def get_locale():
        # If user has set a language preference in the session
        if 'language' in session:
            return session['language']
        # Otherwise, try to detect from request
        return request.accept_languages.best_match(app.config['LANGUAGES'])

    # Handle 404 errors
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Handle 500 errors
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        return dict(app=app, db=db)

    return app

# Import models to ensure they are registered with SQLAlchemy
from app.auth.models import User
from app.modules.health.models import HealthSurvey
from app.modules.mental.models import MentalWellness
from app.modules.fitness.models import FitnessMetric