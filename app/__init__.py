# Flask app will be instantiated here.
# All the flask-plugins will be imported and instantiated here.
# All the routes and blueprints of the application will be added to the application context here.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import config
from app.database import db

def init_app():

    # Initalize the Core Application
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config.LocalDevelopmentConfig)

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():

        from .learning_path import lp_bp
        from .course import course_bp
        from .student import student_bp

        app.register_blueprint(lp_bp)
        app.register_blueprint(course_bp)
        app.register_blueprint(student_bp)

        return app