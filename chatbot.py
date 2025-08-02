import re
import random
import json
import logging
from typing import Dict, List, Tuple
from datetime import datetime
from ai_engine import get_chatbot_response, ai_engine
from app import db
from models import ChatbotTraining, KnowledgeBase

class DrugDiscoveryBot:
    def __init__(self):
        self.knowledge_base = {
            'molecular_analysis': {
                'keywords': ['smiles', 'inchi', 'molecular', 'structure', 'formula', 'weight', 'analyze'],
                'responses': [
                    "To analyze a molecular structure, you can input SMILES or InChI notation in the Molecular Analysis section. The system will calculate properties like molecular weight, formula, and generate 2D structures.",
                    "SMILES (Simplified Molecular Input Line Entry System) is a notation for describing molecular structures. For example, 'CCO' represents ethanol.",
                    "InChI (International Chemical Identifier) provides a standardized way to represent molecular structures with detailed stereochemistry information.",
                    "Molecular weight is calculated from the sum of atomic weights of all atoms in the molecule. This is crucial for dosage calculations.",
                ]
            },
            'drug_formulation': {
                'keywords': ['formulation', 'excipient', 'tablet', 'capsule', 'injection', 'dosage', 'binder', 'disintegrant'],
                'responses': [
                    "Drug formulation involves selecting appropriate excipients based on the active pharmaceutical ingredient (API) properties. Consider factors like solubility, stability, and bioavailability.",
                    "Common excipients include binders (microcrystalline cellulose), disintegrants (croscarmellose sodium), and lubricants (magnesium stearate).",
                    "For poorly soluble drugs, consider solubilizing excipients like cyclodextrins or surfactants.",
                    "Tablet formulation requires balancing compressibility, disintegration time, and drug release profile.",
                ]
            },
            'pharmacology': {
                'keywords': ['mechanism', 'action', 'receptor', 'enzyme', 'inhibitor', 'agonist', 'antagonist', 'bioavailability'],
                'responses': [
                    "Drug mechanisms of action involve interaction with specific molecular targets like receptors, enzymes, or ion channels.",
                    "Agonists activate receptors, while antagonists block receptor activation. Partial agonists have intermediate activity.",
                    "Enzyme inhibitors can be competitive (reversible) or non-competitive (irreversible), affecting drug efficacy and duration.",
                    "Bioavailability is affected by factors like first-pass metabolism, drug solubility, and formulation properties.",
                ]
            },
            'toxicology': {
                'keywords': ['toxicity', 'side effects', 'adverse', 'safety', 'ld50', 'therapeutic index'],
                'responses': [
                    "Toxicology assessment includes acute toxicity (LD50), chronic toxicity, and organ-specific effects.",
                    "Therapeutic index (TI) is the ratio of toxic dose to effective dose. Higher TI indicates safer drugs.",
                    "Common side effects include gastrointestinal, cardiovascular, and central nervous system effects.",
                    "Drug interactions can increase toxicity through enzyme inhibition or competition for binding sites.",
                ]
            },
            'regulatory': {
                'keywords': ['fda', 'ema', 'regulatory', 'approval', 'clinical trials', 'ich', 'gmp'],
                'responses': [
                    "Drug approval requires preclinical studies, Phase I-III clinical trials, and regulatory submission (NDA/BLA).",
                    "ICH guidelines provide international standards for drug development, including stability, impurities, and efficacy.",
                    "Good Manufacturing Practice (GMP) ensures consistent quality during drug production.",
                    "Regulatory pathways vary by region: FDA (US), EMA (Europe), PMDA (Japan), with some harmonized requirements.",
                ]
            },
            'patents': {
                'keywords': ['patent', 'intellectual property', 'generic', 'exclusivity', 'prior art'],
                'responses': [
                    "Patent searches should cover composition, method of use, and formulation patents before developing new drugs.",
                    "Generic drugs can be developed after patent expiry, but must demonstrate bioequivalence to the reference product.",
                    "Patent landscapes include composition of matter, method of treatment, and formulation patents with different expiry dates.",
                    "Freedom to operate (FTO) analysis identifies potential patent infringement risks during development.",
                ]
            }
        }
        
        self.general_responses = [
            "I'm here to help with drug discovery questions. You can ask about molecular analysis, formulation, pharmacology, toxicology, regulatory affairs, or patents.",
            "For specific molecular analysis, please use the Molecular Analysis tool. For drug information, check the Drug Database.",
            "The Excipients Library contains detailed information about pharmaceutical excipients and their compatibility.",
            "I can provide general guidance, but always consult current literature and regulatory guidelines for specific projects.",
        ]
        
        self.greeting_keywords = ['hello', 'hi', 'hey', 'greetings']
        self.greeting_responses = [
            "Hello! I'm the MutaSight AI Assistant. How can I help you with your drug discovery project today?",
            "Hi there! I'm here to assist with molecular analysis, formulation, and drug discovery questions.",
            "Greetings! What would you like to know about drug discovery and development?",
        ]

    def get_response(self, query: str, context=None) -> str:
        """Generate a response based on the user query using AI engine"""
        try:
            # First try the advanced AI engine
            ai_response = get_chatbot_response(query, context)
            
            if ai_response and ai_response != "I apologize, but I'm experiencing technical difficulties. Please try again.":
                # Store successful interaction for training
                self._store_interaction(query, ai_response, context, 'positive')
                return ai_response
            
            # Fallback to rule-based system
            query_lower = query.lower()
            
            # Check for greetings
            if any(greeting in query_lower for greeting in self.greeting_keywords):
                response = random.choice(self.greeting_responses)
                self._store_interaction(query, response, context, 'neutral')
                return response
            
            # Find matching knowledge area
            best_match = self._find_best_match(query_lower)
            
            if best_match:
                category, confidence = best_match
                if confidence > 0.3:  # Threshold for relevance
                    response = random.choice(self.knowledge_base[category]['responses'])
                    self._store_interaction(query, response, context, 'positive')
                    return response
            
            # Specific pattern matching for common queries
            specific_response = self._get_specific_response(query_lower)
            if specific_response:
                self._store_interaction(query, specific_response, context, 'positive')
                return specific_response
            
            # Enhanced default response with drug discovery focus
            enhanced_response = self._get_enhanced_default_response(query)
            self._store_interaction(query, enhanced_response, context, 'neutral')
            return enhanced_response
            
        except Exception as e:
            logging.error(f"Error in chatbot get_response: {e}")
            return "I'm experiencing some technical difficulties. Please try rephrasing your question."

    def _find_best_match(self, query: str) -> Tuple[str, float]:
        """Find the best matching knowledge category"""
        best_category = None
        best_score = 0
        
        for category, data in self.knowledge_base.items():
            score = 0
            for keyword in data['keywords']:
                if keyword in query:
                    score += 1
            
            # Normalize score by number of keywords
            normalized_score = score / len(data['keywords'])
            
            if normalized_score > best_score:
                best_score = normalized_score
                best_category = category
        
        return (best_category, best_score) if best_category else (None, 0)

    def _get_specific_response(self, query: str) -> str:
        """Handle specific query patterns"""
        
        # Molecular weight calculation
        if 'molecular weight' in query or 'mw' in query:
            return "Molecular weight is calculated by summing the atomic weights of all atoms in the molecule. Use the Molecular Analysis tool to automatically calculate MW from SMILES or InChI input."
        
        # SMILES notation
        if 'smiles' in query and ('example' in query or 'format' in query):
            return "SMILES examples: 'CCO' (ethanol), 'CC(=O)O' (acetic acid), 'c1ccccc1' (benzene), 'CC(C)CC1=CC=C(C=C1)C(C)C(=O)O' (ibuprofen)."
        
        # LogP calculation
        if 'logp' in query or 'lipophilicity' in query:
            return "LogP measures lipophilicity (fat solubility). Values between 1-3 are often optimal for oral bioavailability. Higher values may indicate poor solubility."
        
        # Bioavailability
        if 'bioavailability' in query or 'absorption' in query:
            return "Bioavailability depends on solubility, permeability, first-pass metabolism, and formulation. Lipinski's Rule of Five helps predict oral bioavailability."
        
        # Drug-drug interactions
        if 'interaction' in query or 'cyp' in query:
            return "Drug interactions often involve CYP450 enzymes. CYP3A4, 2D6, and 2C9 are major drug-metabolizing enzymes. Check for inhibition or induction potential."
        
        # Clinical trials
        if 'clinical trial' in query or 'phase' in query:
            return "Clinical trials have 4 phases: Phase I (safety, dose), Phase II (efficacy, side effects), Phase III (large-scale efficacy), Phase IV (post-market surveillance)."
        
        return None

    def add_custom_knowledge(self, category: str, keywords: List[str], responses: List[str]):
        """Add custom knowledge to the bot"""
        self.knowledge_base[category] = {
            'keywords': keywords,
            'responses': responses
        }

    def get_available_topics(self) -> List[str]:
        """Return list of available knowledge topics"""
        return list(self.knowledge_base.keys())
    
    def _store_interaction(self, query: str, response: str, context, feedback: str):
        """Store interaction for training purposes"""
        try:
            # Determine topic category
            topic_category = self._classify_query_topic(query)
            
            interaction = ChatbotTraining(
                user_query=query,
                bot_response=response,
                user_feedback=feedback,
                context_data=json.dumps(context) if context else None,
                topic_category=topic_category,
                response_accuracy=0.8 if feedback == 'positive' else 0.3
            )
            
            db.session.add(interaction)
            db.session.commit()
            
        except Exception as e:
            logging.error(f"Error storing chatbot interaction: {e}")
            try:
                db.session.rollback()
            except:
                pass
    
    def _classify_query_topic(self, query: str) -> str:
        """Classify query topic for training"""
        query_lower = query.lower()
        
        # Check against existing knowledge base categories
        for category in self.knowledge_base.keys():
            if any(keyword in query_lower for keyword in self.knowledge_base[category]['keywords']):
                return category
        
        # Additional classification
        if any(word in query_lower for word in ['drug', 'compound', 'molecule', 'discovery']):
            return 'drug_discovery'
        elif any(word in query_lower for word in ['toxic', 'safety', 'adverse']):
            return 'toxicology'
        else:
            return 'general'
    
    def _get_enhanced_default_response(self, query: str) -> str:
        """Generate enhanced default response based on query content"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['compound', 'molecule', 'chemical']):
            return "I can help you analyze molecular compounds using SMILES or InChI notation. Try using the Molecular Analysis tool, or ask me about specific molecular properties like molecular weight, LogP, or structural features."
        
        elif any(word in query_lower for word in ['drug', 'medicine', 'pharmaceutical']):
            return "I can assist with drug-related questions including mechanisms of action, formulation, pharmacokinetics, and regulatory requirements. What specific aspect of drug development are you interested in?"
        
        elif any(word in query_lower for word in ['formula', 'formulation', 'excipient']):
            return "For drug formulation questions, I can help with excipient selection, compatibility, dosage forms, and formulation strategies. Check the Excipients Library for detailed compatibility data."
        
        elif any(word in query_lower for word in ['toxic', 'safety', 'adverse']):
            return "I can provide information about drug safety, toxicity assessment, side effects, and risk evaluation. What specific safety concern would you like to discuss?"
        
        elif any(word in query_lower for word in ['predict', 'calculate', 'analyze']):
            return "I can help with various predictions and calculations including molecular properties, drug-drug interactions, ADMET properties, and toxicity predictions. What would you like me to predict or calculate?"
        
        else:
            return random.choice(self.general_responses)
    
    def train_from_interactions(self):
        """Train chatbot from stored interactions"""
        try:
            # Get positive feedback interactions for training
            positive_interactions = ChatbotTraining.query.filter_by(
                user_feedback='positive',
                is_training_data=True
            ).all()
            
            if len(positive_interactions) > 10:
                # Update AI engine with successful interactions
                ai_engine.retrain_models()
                logging.info(f"Retrained chatbot with {len(positive_interactions)} positive interactions")
                return True
            else:
                logging.info("Insufficient training data for retraining")
                return False
                
        except Exception as e:
            logging.error(f"Error training from interactions: {e}")
            return False
    
    def get_response_with_confidence(self, query: str, context=None) -> Tuple[str, float]:
        """Get response with confidence score"""
        try:
            response = self.get_response(query, context)
            
            # Calculate confidence based on match quality
            query_lower = query.lower()
            best_match = self._find_best_match(query_lower)
            
            if best_match and best_match[1] > 0.5:
                confidence = 0.9
            elif self._get_specific_response(query_lower):
                confidence = 0.8
            elif any(greeting in query_lower for greeting in self.greeting_keywords):
                confidence = 0.95
            else:
                confidence = 0.6
            
            return response, confidence
            
        except Exception as e:
            logging.error(f"Error getting response with confidence: {e}")
            return "I apologize for the technical difficulty.", 0.3
