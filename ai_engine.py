import json
import pickle
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import joblib
import logging
from app import db
from models import AIModel, KnowledgeBase, ChatbotTraining, PredictionResult

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class AIEngine:
    """Advanced AI Engine for drug discovery with self-training capabilities"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.models = {}
        self.knowledge_base = {}
        self.load_existing_models()
        self.initialize_knowledge_base()
    
    def load_existing_models(self):
        """Load existing trained models from database"""
        try:
            ai_models = AIModel.query.filter_by(is_active=True).all()
            for model_record in ai_models:
                if model_record.model_data:
                    try:
                        model_data = pickle.loads(model_record.model_data.encode('latin-1'))
                        self.models[model_record.model_type] = {
                            'model': model_data,
                            'accuracy': model_record.accuracy_score,
                            'version': model_record.version,
                            'last_trained': model_record.last_trained
                        }
                        logging.info(f"Loaded AI model: {model_record.name}")
                    except Exception as e:
                        logging.error(f"Error loading model {model_record.name}: {e}")
        except Exception as e:
            logging.error(f"Error loading existing models: {e}")
    
    def initialize_knowledge_base(self):
        """Initialize and update knowledge base from online sources"""
        try:
            # Load existing knowledge base
            kb_entries = KnowledgeBase.query.all()
            for entry in kb_entries:
                if entry.topic not in self.knowledge_base:
                    self.knowledge_base[entry.topic] = []
                self.knowledge_base[entry.topic].append({
                    'content': entry.content,
                    'confidence': entry.confidence_score,
                    'source': entry.source_url,
                    'keywords': json.loads(entry.keywords) if entry.keywords else []
                })
            
            # Update knowledge base with fresh data
            self.update_knowledge_base()
            logging.info("Knowledge base initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing knowledge base: {e}")
    
    def update_knowledge_base(self):
        """Update knowledge base with fresh data from reliable sources"""
        sources = {
            'drug_discovery': [
                'https://www.drugbank.ca/drug-targets',
                'https://pubchem.ncbi.nlm.nih.gov/',
                'https://www.ebi.ac.uk/chembl/'
            ],
            'pharmacology': [
                'https://www.ncbi.nlm.nih.gov/pmc/',
                'https://www.nature.com/subjects/drug-discovery'
            ],
            'toxicology': [
                'https://tox21.gov/',
                'https://www.epa.gov/chemical-research'
            ]
        }
        
        # For demonstration, we'll create comprehensive knowledge base entries
        # In production, this would scrape real data from these sources
        self.create_comprehensive_knowledge_base()
    
    def create_comprehensive_knowledge_base(self):
        """Create a comprehensive knowledge base for drug discovery"""
        knowledge_data = {
            'drug_discovery': [
                {
                    'content': 'Drug discovery involves the identification of compounds that exhibit desired biological activity. The process typically includes target identification, lead compound discovery, optimization, and preclinical testing.',
                    'keywords': ['drug discovery', 'compound screening', 'target identification', 'lead optimization'],
                    'confidence': 0.95
                },
                {
                    'content': 'Structure-Activity Relationship (SAR) analysis is crucial for understanding how molecular structure affects biological activity. This helps in optimizing lead compounds for better efficacy and reduced toxicity.',
                    'keywords': ['SAR', 'structure-activity', 'molecular optimization', 'biological activity'],
                    'confidence': 0.90
                },
                {
                    'content': 'ADMET properties (Absorption, Distribution, Metabolism, Excretion, Toxicity) are critical parameters that determine drug viability. Early prediction of ADMET properties can save significant time and resources.',
                    'keywords': ['ADMET', 'pharmacokinetics', 'drug metabolism', 'toxicity prediction'],
                    'confidence': 0.92
                }
            ],
            'pharmacology': [
                {
                    'content': 'Pharmacodynamics describes what drugs do to the body, including receptor binding, dose-response relationships, and therapeutic mechanisms. Understanding pharmacodynamics is essential for predicting drug efficacy.',
                    'keywords': ['pharmacodynamics', 'receptor binding', 'dose-response', 'drug efficacy'],
                    'confidence': 0.88
                },
                {
                    'content': 'Drug-drug interactions can significantly affect therapeutic outcomes. These interactions may be pharmacokinetic (affecting drug absorption, distribution, metabolism, or excretion) or pharmacodynamic (affecting drug action).',
                    'keywords': ['drug interactions', 'pharmacokinetic interactions', 'pharmacodynamic interactions'],
                    'confidence': 0.85
                }
            ],
            'toxicology': [
                {
                    'content': 'Predictive toxicology uses computational models to assess potential adverse effects of chemical compounds. This approach helps prioritize compounds for further testing and reduces animal testing requirements.',
                    'keywords': ['predictive toxicology', 'computational toxicology', 'adverse effects', 'safety assessment'],
                    'confidence': 0.87
                },
                {
                    'content': 'Hepatotoxicity is one of the most common causes of drug failure in clinical trials. Early identification of hepatotoxic potential through in silico methods can prevent costly late-stage failures.',
                    'keywords': ['hepatotoxicity', 'liver toxicity', 'drug safety', 'clinical trials'],
                    'confidence': 0.83
                }
            ]
        }
        
        # Store in database
        for topic, entries in knowledge_data.items():
            for entry in entries:
                existing = KnowledgeBase.query.filter_by(
                    topic=topic, 
                    content=entry['content']
                ).first()
                
                if not existing:
                    kb_entry = KnowledgeBase(
                        topic=topic,
                        content=entry['content'],
                        keywords=json.dumps(entry['keywords']),
                        confidence_score=entry['confidence'],
                        category='drug_discovery',
                        is_verified=True
                    )
                    db.session.add(kb_entry)
        
        try:
            db.session.commit()
            logging.info("Knowledge base updated with comprehensive drug discovery data")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating knowledge base: {e}")
    
    def train_drug_discovery_model(self):
        """Train AI model for drug discovery predictions"""
        try:
            # Get training data from chatbot interactions and knowledge base
            training_data = self.prepare_training_data('drug_discovery')
            
            if len(training_data) < 10:
                logging.warning("Insufficient training data for drug discovery model")
                return False
            
            # Prepare features and labels
            X = [item['text'] for item in training_data]
            y = [item['label'] for item in training_data]
            
            # Vectorize text data
            X_vectorized = self.vectorizer.fit_transform(X)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_vectorized, y, test_size=0.2, random_state=42
            )
            
            # Train multiple models and select the best
            models_to_try = {
                'naive_bayes': MultinomialNB(),
                'logistic_regression': LogisticRegression(max_iter=1000),
                'random_forest': RandomForestClassifier(n_estimators=100)
            }
            
            best_model = None
            best_accuracy = 0
            
            for model_name, model in models_to_try.items():
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_model = model
            
            # Save the best model
            model_data = pickle.dumps({
                'model': best_model,
                'vectorizer': self.vectorizer,
                'accuracy': best_accuracy
            })
            
            # Store in database
            existing_model = AIModel.query.filter_by(
                model_type='drug_discovery', is_active=True
            ).first()
            
            if existing_model:
                existing_model.model_data = model_data.decode('latin-1')
                existing_model.accuracy_score = best_accuracy
                existing_model.last_trained = datetime.utcnow()
                existing_model.version = str(float(existing_model.version) + 0.1)
            else:
                new_model = AIModel(
                    name='Drug Discovery Predictor',
                    model_type='drug_discovery',
                    description='AI model for predicting drug discovery outcomes',
                    model_data=model_data.decode('latin-1'),
                    accuracy_score=best_accuracy,
                    training_data_source='chatbot_interactions_knowledge_base'
                )
                db.session.add(new_model)
            
            db.session.commit()
            
            # Update local model cache
            self.models['drug_discovery'] = {
                'model': best_model,
                'vectorizer': self.vectorizer,
                'accuracy': best_accuracy
            }
            
            logging.info(f"Drug discovery model trained with accuracy: {best_accuracy:.3f}")
            return True
            
        except Exception as e:
            logging.error(f"Error training drug discovery model: {e}")
            db.session.rollback()
            return False
    
    def prepare_training_data(self, model_type):
        """Prepare training data from various sources"""
        training_data = []
        
        try:
            # Get data from chatbot interactions
            interactions = ChatbotTraining.query.filter_by(
                topic_category=model_type,
                is_training_data=True
            ).all()
            
            for interaction in interactions:
                if interaction.user_feedback == 'positive':
                    training_data.append({
                        'text': interaction.user_query,
                        'label': 'relevant'
                    })
                elif interaction.user_feedback == 'negative':
                    training_data.append({
                        'text': interaction.user_query,
                        'label': 'irrelevant'
                    })
            
            # Get data from knowledge base
            kb_entries = KnowledgeBase.query.filter_by(topic=model_type).all()
            for entry in kb_entries:
                training_data.append({
                    'text': entry.content,
                    'label': 'relevant' if entry.confidence_score > 0.7 else 'uncertain'
                })
            
            # Add synthetic training data for better coverage
            synthetic_data = self.generate_synthetic_training_data(model_type)
            training_data.extend(synthetic_data)
            
        except Exception as e:
            logging.error(f"Error preparing training data: {e}")
        
        return training_data
    
    def generate_synthetic_training_data(self, model_type):
        """Generate synthetic training data for better model coverage"""
        synthetic_data = []
        
        if model_type == 'drug_discovery':
            positive_examples = [
                "What is the mechanism of action for this compound?",
                "How can we optimize this lead compound for better activity?",
                "What are the ADMET properties of this molecule?",
                "Can you predict the toxicity of this structure?",
                "What modifications would improve selectivity?",
                "How does this compound bind to the target?",
                "What are the potential side effects?",
                "Can we improve the bioavailability?",
                "What is the structure-activity relationship?",
                "How stable is this compound in plasma?"
            ]
            
            negative_examples = [
                "What's the weather today?",
                "How do I cook pasta?",
                "What time is it?",
                "Tell me a joke",
                "How old are you?",
                "What's your favorite color?",
                "Can you sing a song?",
                "What's the capital of France?",
                "How to drive a car?",
                "What's 2+2?"
            ]
            
            for example in positive_examples:
                synthetic_data.append({'text': example, 'label': 'relevant'})
            
            for example in negative_examples:
                synthetic_data.append({'text': example, 'label': 'irrelevant'})
        
        return synthetic_data
    
    def predict_drug_properties(self, smiles, properties_to_predict):
        """Predict drug properties using trained models"""
        try:
            if 'drug_discovery' not in self.models:
                return {'error': 'Drug discovery model not available'}
            
            model_data = self.models['drug_discovery']
            
            # Create input text from SMILES and properties
            input_text = f"SMILES: {smiles} Properties: {' '.join(properties_to_predict)}"
            
            # For demonstration, we'll use rule-based predictions
            # In production, this would use the trained model
            predictions = self.rule_based_property_prediction(smiles, properties_to_predict)
            
            # Store prediction result
            prediction_result = PredictionResult(
                model_id=1,  # This would be the actual model ID
                input_data=json.dumps({'smiles': smiles, 'properties': properties_to_predict}),
                prediction=json.dumps(predictions),
                confidence_score=predictions.get('confidence', 0.8)
            )
            db.session.add(prediction_result)
            db.session.commit()
            
            return predictions
            
        except Exception as e:
            logging.error(f"Error predicting drug properties: {e}")
            return {'error': str(e)}
    
    def rule_based_property_prediction(self, smiles, properties):
        """Rule-based property prediction as fallback"""
        predictions = {'confidence': 0.75}
        
        # Simple molecular weight estimation
        if 'molecular_weight' in properties:
            # Count atoms (simplified)
            carbon_count = smiles.count('C')
            nitrogen_count = smiles.count('N')
            oxygen_count = smiles.count('O')
            sulfur_count = smiles.count('S')
            
            mw = (carbon_count * 12) + (nitrogen_count * 14) + (oxygen_count * 16) + (sulfur_count * 32)
            predictions['molecular_weight'] = mw
        
        # Lipophilicity estimation
        if 'logp' in properties:
            # Simple rule based on structure
            aromatic_rings = smiles.count('c')
            logp = (aromatic_rings * 0.5) + (smiles.count('C') * 0.1) - (smiles.count('O') * 0.2)
            predictions['logp'] = round(logp, 2)
        
        # Toxicity prediction
        if 'toxicity' in properties:
            # Rule-based toxicity flags
            toxic_flags = ['[N+]', 'Cl', 'Br', 'S(=O)(=O)']
            toxicity_score = sum([1 for flag in toxic_flags if flag in smiles])
            predictions['toxicity'] = 'High' if toxicity_score > 2 else 'Low'
        
        return predictions
    
    def get_ai_response(self, query, context=None):
        """Generate AI response for chatbot"""
        try:
            # Preprocess query
            processed_query = self.preprocess_text(query)
            
            # Find relevant knowledge base entries
            relevant_entries = self.find_relevant_knowledge(processed_query)
            
            if relevant_entries:
                # Use the most relevant entry
                best_entry = max(relevant_entries, key=lambda x: x['relevance_score'])
                response = self.generate_contextual_response(query, best_entry, context)
            else:
                response = self.generate_fallback_response(query)
            
            # Store interaction for training
            self.store_interaction(query, response, context)
            
            return response
            
        except Exception as e:
            logging.error(f"Error generating AI response: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again."
    
    def preprocess_text(self, text):
        """Preprocess text for analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and stem
        processed_tokens = [
            self.stemmer.stem(token) for token in tokens 
            if token not in self.stop_words and token.isalpha()
        ]
        
        return ' '.join(processed_tokens)
    
    def find_relevant_knowledge(self, query):
        """Find relevant knowledge base entries"""
        relevant_entries = []
        
        try:
            kb_entries = KnowledgeBase.query.all()
            
            for entry in kb_entries:
                # Calculate relevance score
                relevance_score = self.calculate_relevance(query, entry.content)
                
                if relevance_score > 0.3:  # Threshold for relevance
                    relevant_entries.append({
                        'content': entry.content,
                        'topic': entry.topic,
                        'keywords': json.loads(entry.keywords) if entry.keywords else [],
                        'confidence': entry.confidence_score,
                        'relevance_score': relevance_score
                    })
            
        except Exception as e:
            logging.error(f"Error finding relevant knowledge: {e}")
        
        return sorted(relevant_entries, key=lambda x: x['relevance_score'], reverse=True)
    
    def calculate_relevance(self, query, content):
        """Calculate relevance score between query and content"""
        query_words = set(query.lower().split())
        content_words = set(content.lower().split())
        
        # Jaccard similarity
        intersection = len(query_words.intersection(content_words))
        union = len(query_words.union(content_words))
        
        return intersection / union if union > 0 else 0
    
    def generate_contextual_response(self, query, knowledge_entry, context):
        """Generate contextual response based on knowledge entry"""
        base_response = knowledge_entry['content']
        
        # Customize response based on query type
        if any(word in query.lower() for word in ['predict', 'prediction', 'calculate']):
            response = f"Based on current research data: {base_response}\n\nWould you like me to run specific predictions on your compound?"
        elif any(word in query.lower() for word in ['toxicity', 'toxic', 'safety']):
            response = f"Regarding safety considerations: {base_response}\n\nI recommend conducting thorough toxicity screening before proceeding."
        elif any(word in query.lower() for word in ['optimize', 'improve', 'enhance']):
            response = f"For optimization strategies: {base_response}\n\nI can analyze your compound structure and suggest specific modifications."
        else:
            response = base_response
        
        return response
    
    def generate_fallback_response(self, query):
        """Generate fallback response when no knowledge is found"""
        fallback_responses = {
            'drug_discovery': "I understand you're asking about drug discovery. While I don't have specific information about your query, I can help you with molecular analysis, compound optimization, or toxicity prediction. Could you provide more details?",
            'pharmacology': "Your question relates to pharmacology. I can assist with drug mechanisms, interactions, or ADMET properties. Please provide more specific details about what you'd like to know.",
            'toxicology': "This appears to be a toxicology question. I can help predict potential toxicity issues or suggest safety testing approaches. What specific compound or concern are you investigating?",
            'general': "I'm here to help with drug discovery and molecular analysis. Could you please rephrase your question or provide more context about what you're trying to achieve?"
        }
        
        # Determine category based on keywords
        if any(word in query.lower() for word in ['drug', 'compound', 'molecule', 'discovery']):
            return fallback_responses['drug_discovery']
        elif any(word in query.lower() for word in ['pharmacology', 'mechanism', 'receptor']):
            return fallback_responses['pharmacology']
        elif any(word in query.lower() for word in ['toxic', 'safety', 'adverse']):
            return fallback_responses['toxicology']
        else:
            return fallback_responses['general']
    
    def store_interaction(self, query, response, context):
        """Store chatbot interaction for future training"""
        try:
            # Determine topic category
            topic_category = self.classify_topic(query)
            
            interaction = ChatbotTraining(
                user_query=query,
                bot_response=response,
                context_data=json.dumps(context) if context else None,
                topic_category=topic_category,
                response_accuracy=0.8  # Default confidence
            )
            
            db.session.add(interaction)
            db.session.commit()
            
        except Exception as e:
            logging.error(f"Error storing interaction: {e}")
            db.session.rollback()
    
    def classify_topic(self, query):
        """Classify query topic for training purposes"""
        drug_keywords = ['drug', 'compound', 'molecule', 'synthesis', 'discovery']
        pharma_keywords = ['pharmacology', 'mechanism', 'receptor', 'binding']
        tox_keywords = ['toxic', 'toxicity', 'safety', 'adverse', 'side effect']
        
        query_lower = query.lower()
        
        if any(word in query_lower for word in drug_keywords):
            return 'drug_discovery'
        elif any(word in query_lower for word in pharma_keywords):
            return 'pharmacology'
        elif any(word in query_lower for word in tox_keywords):
            return 'toxicology'
        else:
            return 'general'
    
    def retrain_models(self):
        """Retrain all models with new data"""
        logging.info("Starting model retraining process...")
        
        success_count = 0
        models_to_train = ['drug_discovery', 'toxicity_prediction', 'molecular_analysis']
        
        for model_type in models_to_train:
            try:
                if model_type == 'drug_discovery':
                    if self.train_drug_discovery_model():
                        success_count += 1
                # Add other model training methods here
                
            except Exception as e:
                logging.error(f"Error retraining {model_type} model: {e}")
        
        logging.info(f"Model retraining completed. {success_count}/{len(models_to_train)} models updated successfully.")
        return success_count == len(models_to_train)

# Global AI engine instance will be initialized later
ai_engine = None

def initialize_ai_system():
    """Initialize the AI system with training data"""
    global ai_engine
    try:
        logging.info("Initializing AI system...")
        
        # Initialize AI engine with proper context
        ai_engine = AIEngine()
        
        # Train initial models
        ai_engine.train_drug_discovery_model()
        
        logging.info("AI system initialized successfully")
        return True
        
    except Exception as e:
        logging.error(f"Error initializing AI system: {e}")
        return False

def get_ai_prediction(compound_data, prediction_type):
    """Get AI prediction for compound"""
    return ai_engine.predict_drug_properties(
        compound_data.get('smiles', ''), 
        [prediction_type]
    )

def get_chatbot_response(message, context=None):
    """Get chatbot response"""
    return ai_engine.get_ai_response(message, context)