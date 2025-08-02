import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.secret_key = os.environ.get("SESSION_SECRET")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    # Configure upload folder
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Apply proxy fix for proper URL generation
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Create tables
    with app.app_context():
        import models  # noqa: F401
        db.create_all()
        
        # Initialize default data
        from data.drug_database import initialize_drug_data
        from data.excipients_data import initialize_excipients_data
        initialize_drug_data()
        initialize_excipients_data()
        
        # Initialize AI system and comprehensive database
        try:
            from ai_engine import initialize_ai_system
            from data_scraper import initialize_comprehensive_database
            
            # Initialize AI system with proper context
            initialize_ai_system()
            
            # Initialize comprehensive drug discovery database
            initialize_comprehensive_database()
            
            logging.info("AI system and comprehensive database initialized")
        except Exception as e:
            logging.error(f"Error initializing AI system: {e}")
        
        logging.info("Database tables created and initialized")
    
    # Register blueprints
    from auth import auth_bp
    from routes import main_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    
    return app

# Create app instance
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))
