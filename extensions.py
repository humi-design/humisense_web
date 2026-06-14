from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Configure login manager
login_manager.login_view = 'admin.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


def init_extensions(app):
    """Initialize Flask extensions with the app."""
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    @login_manager.user_loader
    def load_user(user_id):
        # Import here to avoid circular imports
        from models import User
        return User.query.get(int(user_id))
    
    return db