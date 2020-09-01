"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, login_user, current_user, logout_user,
                        login_required)
import locale
import os
from dotenv import load_dotenv




locale.setlocale(locale.LC_ALL, 'en_US.utf8')

db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path='.env')

def create_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)
    # Initialize login manager
    login = LoginManager(app)
    login.init_app(app)

    ###############################################################################
    # Given *user_id*, return the associated User object.
    # :param unicode user_id: user_id (email) user to retrieve
    ###############################################################################
    from .auth.models import users
    @login.user_loader
    def user_loader(user_id):
        """Given *user_id*, return the associated User object.

        :param unicode user_id: user_id (email) user to retrieve

        """
        return users.query.get(user_id)


    with app.app_context():
        # Import parts of our application
        from .auth import auth
        from .trans import trans
        from .stats import stats
        from .profile import profile

        # Register Blueprints
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(trans.trans_bp)
        app.register_blueprint(stats.stats_bp)
        app.register_blueprint(profile.profile_bp)

        from .trans.models import trans as trans_c
        from .profile.models import categories, accounts
        db.create_all()  # Create sql tables for our data models

        return app
