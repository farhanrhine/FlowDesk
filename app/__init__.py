import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=None):
    app = Flask(__name__)
    
    if config_class is None:
        if os.environ.get('FLASK_ENV') == 'production':
            from config import ProductionConfig
            config_class = ProductionConfig
        else:
            from config import DevelopmentConfig
            config_class = DevelopmentConfig
    
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.app_context():
        # Create database tables for our models
        db.create_all()
    
    # Register blueprints
    from app.auth import auth
    from app.dashboard import dashboard
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(dashboard)
    
    return app
