from datetime import datetime
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(20), default='researcher')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    projects = db.relationship('Project', backref='owner', lazy=True)
    chat_messages = db.relationship('ChatMessage', backref='author', lazy=True)
    project_memberships = db.relationship('ProjectMember', backref='user', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='active')
    
    # Relationships
    members = db.relationship('ProjectMember', backref='project', lazy=True)
    chat_messages = db.relationship('ChatMessage', backref='project', lazy=True)
    molecular_analyses = db.relationship('MolecularAnalysis', backref='project', lazy=True)

class ProjectMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(20), default='member')  # owner, admin, member
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    message_type = db.Column(db.String(20), default='user')  # user, bot, system

class MolecularAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    smiles = db.Column(db.String(500))
    inchi = db.Column(db.String(1000))
    molecular_formula = db.Column(db.String(200))
    molecular_weight = db.Column(db.Float)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    results = db.Column(db.Text)  # JSON string for analysis results

class DrugData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    generic_name = db.Column(db.String(200))
    brand_names = db.Column(db.Text)  # JSON array
    smiles = db.Column(db.String(500))
    inchi = db.Column(db.String(1000))
    molecular_formula = db.Column(db.String(200))
    molecular_weight = db.Column(db.Float)
    therapeutic_class = db.Column(db.String(100))
    mechanism_of_action = db.Column(db.Text)
    indications = db.Column(db.Text)
    contraindications = db.Column(db.Text)
    side_effects = db.Column(db.Text)
    dosage_forms = db.Column(db.Text)  # JSON array

class Excipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    chemical_name = db.Column(db.String(300))
    cas_number = db.Column(db.String(20))
    function = db.Column(db.String(100))  # binder, disintegrant, etc.
    description = db.Column(db.Text)
    compatibility = db.Column(db.Text)  # JSON object
    toxicity_data = db.Column(db.Text)
    regulatory_status = db.Column(db.String(100))
    typical_concentration = db.Column(db.String(100))
    physical_properties = db.Column(db.Text)  # JSON object

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)  # formulation, regulatory, etc.
    content = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(500))

class AIModel(db.Model):
    """Self-training AI models for drug discovery"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    model_type = db.Column(db.String(50), nullable=False)  # drug_discovery, molecular_analysis, toxicity_prediction
    description = db.Column(db.Text)
    model_data = db.Column(db.Text)  # Pickled model data
    training_data_source = db.Column(db.String(500))
    accuracy_score = db.Column(db.Float)
    last_trained = db.Column(db.DateTime, default=datetime.utcnow)
    version = db.Column(db.String(20), default='1.0')
    is_active = db.Column(db.Boolean, default=True)
    training_status = db.Column(db.String(20), default='trained')  # training, trained, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class KnowledgeBase(db.Model):
    """Knowledge base for AI training and responses"""
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(200), nullable=False)  # drug_discovery, pharmacology, toxicology
    content = db.Column(db.Text, nullable=False)
    source_url = db.Column(db.String(500))
    confidence_score = db.Column(db.Float, default=1.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    keywords = db.Column(db.Text)  # JSON array for search optimization
    category = db.Column(db.String(100))
    is_verified = db.Column(db.Boolean, default=False)

class UserSession(db.Model):
    """Track live users on projects"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    session_id = db.Column(db.String(100), nullable=False, unique=True)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    current_page = db.Column(db.String(200))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))

class ChatbotTraining(db.Model):
    """Training data and interactions for chatbot improvement"""
    id = db.Column(db.Integer, primary_key=True)
    user_query = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    user_feedback = db.Column(db.String(20))  # positive, negative, neutral
    context_data = db.Column(db.Text)  # JSON with conversation context
    response_accuracy = db.Column(db.Float)
    topic_category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_training_data = db.Column(db.Boolean, default=True)

class DrugInteraction(db.Model):
    """Drug-drug interactions database"""
    id = db.Column(db.Integer, primary_key=True)
    drug1_id = db.Column(db.Integer, db.ForeignKey('drug_data.id'), nullable=False)
    drug2_id = db.Column(db.Integer, db.ForeignKey('drug_data.id'), nullable=True)  # Allow NULL for non-drug interactions
    interaction_type = db.Column(db.String(50))  # major, moderate, minor
    description = db.Column(db.Text)
    clinical_significance = db.Column(db.Text)
    mechanism = db.Column(db.Text)
    management = db.Column(db.Text)
    severity_level = db.Column(db.Integer, default=1)  # 1-5 scale
    evidence_level = db.Column(db.String(20))  # established, probable, possible
    
class CompoundSimilarity(db.Model):
    """Store molecular similarity calculations for faster retrieval"""
    id = db.Column(db.Integer, primary_key=True)
    compound1_smiles = db.Column(db.String(500), nullable=False)
    compound2_smiles = db.Column(db.String(500), nullable=False)
    similarity_score = db.Column(db.Float, nullable=False)
    similarity_method = db.Column(db.String(50), default='tanimoto')
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class PredictionResult(db.Model):
    """Store AI model predictions"""
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('ai_model.id'), nullable=False)
    input_data = db.Column(db.Text, nullable=False)  # JSON with input parameters
    prediction = db.Column(db.Text, nullable=False)  # JSON with prediction results
    confidence_score = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    validated = db.Column(db.Boolean, default=False)
    actual_outcome = db.Column(db.Text)  # For model retraining
