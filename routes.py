import json
import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from flask_socketio import emit, join_room, leave_room
from werkzeug.utils import secure_filename
from app import db, socketio
from models import (Project, ProjectMember, ChatMessage, MolecularAnalysis, DrugData, Excipient, Report, 
                   UserSession, AIModel, KnowledgeBase, DrugInteraction, PredictionResult)
from molecular_utils import analyze_molecule, generate_2d_structure
from chatbot import DrugDiscoveryBot
from report_generator import generate_pdf_report
from live_tracking import create_live_tracker
from ai_engine import get_ai_prediction, get_chatbot_response, ai_engine

main_bp = Blueprint('main', __name__)
bot = DrugDiscoveryBot()

# Initialize live user tracker
live_tracker = None

def init_live_tracker():
    global live_tracker
    if live_tracker is None:
        live_tracker = create_live_tracker(socketio)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get user's projects
    user_projects = Project.query.filter_by(owner_id=current_user.id).all()
    member_projects = Project.query.join(ProjectMember).filter(
        ProjectMember.user_id == current_user.id,
        ProjectMember.project_id != Project.id
    ).all()
    
    # Get recent molecular analyses
    recent_analyses = MolecularAnalysis.query.filter_by(user_id=current_user.id)\
        .order_by(MolecularAnalysis.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         user_projects=user_projects,
                         member_projects=member_projects,
                         recent_analyses=recent_analyses)

@main_bp.route('/molecular-analysis')
@login_required
def molecular_analysis():
    return render_template('molecular_analysis.html')

@main_bp.route('/analyze-molecule', methods=['POST'])
@login_required
def analyze_molecule_route():
    data = request.get_json()
    input_type = data.get('input_type', 'smiles')
    input_value = data.get('input_value', '')
    project_id = data.get('project_id')
    
    try:
        # Basic molecular analysis
        results = analyze_molecule(input_value, input_type)
        
        # Enhanced AI predictions if AI engine is available
        if ai_engine:
            try:
                ai_predictions = get_ai_prediction({
                    'smiles': results.get('smiles', input_value)
                }, 'molecular_properties')
                
                if 'error' not in ai_predictions:
                    results['ai_predictions'] = ai_predictions
                    results['prediction_confidence'] = ai_predictions.get('confidence', 0.75)
            except Exception as e:
                results['ai_predictions'] = {'note': 'AI predictions temporarily unavailable'}
        
        # Save analysis to database
        analysis = MolecularAnalysis(
            name=data.get('name', f'Analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}'),
            smiles=results.get('smiles'),
            inchi=results.get('inchi'),
            molecular_formula=results.get('molecular_formula'),
            molecular_weight=results.get('molecular_weight'),
            project_id=project_id if project_id else None,
            user_id=current_user.id,
            results=json.dumps(results)
        )
        db.session.add(analysis)
        db.session.commit()
        
        return jsonify({'success': True, 'data': results, 'analysis_id': analysis.id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@main_bp.route('/ai-predict', methods=['POST'])
@login_required
def ai_predict():
    """Advanced AI predictions for drug discovery"""
    data = request.get_json()
    compound_data = data.get('compound_data', {})
    prediction_types = data.get('prediction_types', [])
    
    try:
        predictions = {}
        
        for pred_type in prediction_types:
            if ai_engine:
                result = get_ai_prediction(compound_data, pred_type)
                predictions[pred_type] = result
            else:
                predictions[pred_type] = {'error': 'AI engine not available'}
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@main_bp.route('/live-users/<int:project_id>')
@login_required
def get_live_users(project_id):
    """Get live users in a project"""
    init_live_tracker()
    
    try:
        # Verify user has access to project
        member = ProjectMember.query.filter_by(
            user_id=current_user.id,
            project_id=project_id
        ).first()
        
        project = Project.query.filter_by(id=project_id, owner_id=current_user.id).first()
        
        if not member and not project:
            return jsonify({'error': 'Access denied'}), 403
        
        active_users = live_tracker.get_project_active_users(project_id) if live_tracker else []
        
        return jsonify({
            'success': True,
            'active_users': active_users,
            'total_count': len(active_users)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@main_bp.route('/join-project-session', methods=['POST'])
@login_required
def join_project_session():
    """Join a project session for live collaboration"""
    data = request.get_json()
    project_id = data.get('project_id')
    
    init_live_tracker()
    
    try:
        # Verify access
        member = ProjectMember.query.filter_by(
            user_id=current_user.id,
            project_id=project_id
        ).first()
        
        project = Project.query.filter_by(id=project_id, owner_id=current_user.id).first()
        
        if not member and not project:
            return jsonify({'error': 'Access denied'}), 403
        
        session_id = live_tracker.start_user_session(current_user.id, project_id) if live_tracker else None
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Joined project session successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@main_bp.route('/drug-database')
@login_required
def drug_database():
    search_query = request.args.get('search', '')
    therapeutic_class = request.args.get('class', '')
    
    query = DrugData.query
    
    if search_query:
        query = query.filter(
            (DrugData.name.ilike(f'%{search_query}%')) |
            (DrugData.generic_name.ilike(f'%{search_query}%'))
        )
    
    if therapeutic_class:
        query = query.filter(DrugData.therapeutic_class.ilike(f'%{therapeutic_class}%'))
    
    drugs = query.all()
    
    # Get unique therapeutic classes for filter
    classes = db.session.query(DrugData.therapeutic_class.distinct()).all()
    therapeutic_classes = [c[0] for c in classes if c[0]]
    
    return render_template('drug_database.html', 
                         drugs=drugs, 
                         therapeutic_classes=therapeutic_classes,
                         search_query=search_query,
                         selected_class=therapeutic_class)

@main_bp.route('/excipients')
@login_required
def excipients():
    search_query = request.args.get('search', '')
    function_filter = request.args.get('function', '')
    
    query = Excipient.query
    
    if search_query:
        query = query.filter(
            (Excipient.name.ilike(f'%{search_query}%')) |
            (Excipient.chemical_name.ilike(f'%{search_query}%'))
        )
    
    if function_filter:
        query = query.filter(Excipient.function.ilike(f'%{function_filter}%'))
    
    excipients = query.all()
    
    # Get unique functions for filter
    functions = db.session.query(Excipient.function.distinct()).all()
    excipient_functions = [f[0] for f in functions if f[0]]
    
    return render_template('excipients.html', 
                         excipients=excipients,
                         excipient_functions=excipient_functions,
                         search_query=search_query,
                         selected_function=function_filter)

@main_bp.route('/projects')
@login_required
def projects():
    user_projects = Project.query.filter_by(owner_id=current_user.id).all()
    member_projects = Project.query.join(ProjectMember).filter(
        ProjectMember.user_id == current_user.id
    ).all()
    
    return render_template('projects.html', 
                         user_projects=user_projects,
                         member_projects=member_projects)

@main_bp.route('/create-project', methods=['POST'])
@login_required
def create_project():
    name = request.form.get('name')
    description = request.form.get('description', '')
    
    if not name:
        flash('Project name is required', 'error')
        return redirect(url_for('main.projects'))
    
    project = Project(
        name=name,
        description=description,
        owner_id=current_user.id
    )
    
    db.session.add(project)
    db.session.commit()
    
    # Add owner as a member
    member = ProjectMember(
        project_id=project.id,
        user_id=current_user.id,
        role='owner'
    )
    db.session.add(member)
    db.session.commit()
    
    flash('Project created successfully', 'success')
    return redirect(url_for('main.projects'))

@main_bp.route('/project/<int:project_id>')
@login_required
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Check if user has access to this project
    is_member = ProjectMember.query.filter_by(
        project_id=project_id,
        user_id=current_user.id
    ).first()
    
    if not is_member and project.owner_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('main.projects'))
    
    analyses = MolecularAnalysis.query.filter_by(project_id=project_id).all()
    messages = ChatMessage.query.filter_by(project_id=project_id)\
        .order_by(ChatMessage.timestamp.asc()).all()
    
    return render_template('chat.html', 
                         project=project,
                         analyses=analyses,
                         messages=messages)

@main_bp.route('/reports')
@login_required
def reports():
    user_reports = Report.query.filter_by(user_id=current_user.id)\
        .order_by(Report.created_at.desc()).all()
    
    return render_template('reports.html', reports=user_reports)

@main_bp.route('/generate-report', methods=['POST'])
@login_required
def generate_report():
    data = request.get_json()
    report_type = data.get('report_type', 'formulation')
    title = data.get('title', 'Drug Discovery Report')
    content = data.get('content', {})
    project_id = data.get('project_id')
    
    try:
        # Generate PDF report
        file_path = generate_pdf_report(title, report_type, content, current_user.username)
        
        # Save report record
        report = Report(
            title=title,
            report_type=report_type,
            content=json.dumps(content),
            project_id=project_id if project_id else None,
            user_id=current_user.id,
            file_path=file_path
        )
        
        db.session.add(report)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'report_id': report.id,
            'download_url': url_for('main.download_report', report_id=report.id)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@main_bp.route('/download-report/<int:report_id>')
@login_required
def download_report(report_id):
    report = Report.query.get_or_404(report_id)
    
    if report.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('main.reports'))
    
    return send_file(report.file_path, as_attachment=True)

# SocketIO events for real-time chat
@socketio.on('join_project')
def on_join(data):
    project_id = data['project_id']
    join_room(f'project_{project_id}')
    emit('status', {'msg': f'{current_user.username} has joined the project chat.'}, 
         room=f'project_{project_id}')

@socketio.on('leave_project')
def on_leave(data):
    project_id = data['project_id']
    leave_room(f'project_{project_id}')
    emit('status', {'msg': f'{current_user.username} has left the project chat.'}, 
         room=f'project_{project_id}')

@socketio.on('send_message')
def handle_message(data):
    project_id = data['project_id']
    content = data['message']
    
    # Save message to database
    message = ChatMessage(
        content=content,
        user_id=current_user.id,
        project_id=project_id,
        message_type='user'
    )
    db.session.add(message)
    db.session.commit()
    
    # Emit to all users in the project room
    emit('receive_message', {
        'message': content,
        'username': current_user.username,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'message_type': 'user'
    }, room=f'project_{project_id}')

@socketio.on('chatbot_query')
def handle_chatbot_query(data):
    project_id = data.get('project_id')
    query = data['query']
    
    # Get bot response
    response = bot.get_response(query)
    
    # Save both user query and bot response
    user_message = ChatMessage(
        content=query,
        user_id=current_user.id,
        project_id=project_id,
        message_type='user'
    )
    
    bot_message = ChatMessage(
        content=response,
        user_id=current_user.id,  # Bot messages associated with user who asked
        project_id=project_id,
        message_type='bot'
    )
    
    db.session.add(user_message)
    db.session.add(bot_message)
    db.session.commit()
    
    # Emit both messages
    emit('receive_message', {
        'message': query,
        'username': current_user.username,
        'timestamp': user_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'message_type': 'user'
    }, room=f'project_{project_id}')
    
    emit('receive_message', {
        'message': response,
        'username': 'MutaSight AI Assistant',
        'timestamp': bot_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'message_type': 'bot'
    }, room=f'project_{project_id}')

# AI Demo and Management Routes
@main_bp.route('/ai-demo')
@login_required
def ai_demo():
    """AI Features Demonstration Page"""
    try:
        # Get AI model statistics
        ai_models = AIModel.query.filter_by(is_active=True).all()
        
        # Get knowledge base statistics
        kb_stats = {}
        kb_entries = KnowledgeBase.query.all()
        for entry in kb_entries:
            topic = entry.topic
            if topic not in kb_stats:
                kb_stats[topic] = 0
            kb_stats[topic] += 1
        
        # Get recent predictions
        recent_predictions = PredictionResult.query.order_by(
            PredictionResult.created_at.desc()
        ).limit(10).all()
        
        # Get active sessions count
        active_sessions = UserSession.query.filter_by(is_active=True).count()
        
        demo_data = {
            'ai_models': [
                {
                    'name': model.name,
                    'type': model.model_type,
                    'accuracy': model.accuracy_score,
                    'version': model.version,
                    'last_trained': model.last_trained.strftime('%Y-%m-%d %H:%M') if model.last_trained else 'Never'
                }
                for model in ai_models
            ],
            'knowledge_stats': kb_stats,
            'recent_predictions': [
                {
                    'id': pred.id,
                    'input_data': str(pred.input_data)[:100] if pred.input_data else '',
                    'confidence': pred.confidence_score,
                    'created_at': pred.created_at.strftime('%H:%M:%S')
                }
                for pred in recent_predictions
            ],
            'active_sessions': active_sessions,
            'total_drugs': DrugData.query.count(),
            'total_excipients': Excipient.query.count(),
            'total_interactions': DrugInteraction.query.count()
        }
        
        return render_template('ai_demo.html', demo_data=demo_data)
        
    except Exception as e:
        flash(f'Error loading AI demo: {str(e)}', 'error')
        return redirect(url_for('main.dashboard'))

@main_bp.route('/retrain-ai', methods=['POST'])
@login_required  
def retrain_ai():
    """Trigger AI model retraining"""
    try:
        if ai_engine:
            success = ai_engine.retrain_models()
            if success:
                return jsonify({
                    'success': True,
                    'message': 'AI models retrained successfully'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Retraining failed or insufficient data'
                })
        else:
            return jsonify({
                'success': False,
                'message': 'AI engine not available'
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@main_bp.route('/knowledge-search', methods=['POST'])
@login_required
def knowledge_search():
    """Search knowledge base"""
    data = request.get_json()
    query = data.get('query', '')
    
    try:
        if not query:
            return jsonify({'success': False, 'error': 'Query is required'})
        
        # Search knowledge base
        results = KnowledgeBase.query.filter(
            KnowledgeBase.content.ilike(f'%{query}%')
        ).order_by(KnowledgeBase.confidence_score.desc()).limit(10).all()
        
        search_results = []
        for result in results:
            search_results.append({
                'topic': result.topic,
                'content': result.content[:200] + '...' if len(result.content) > 200 else result.content,
                'confidence': result.confidence_score,
                'keywords': json.loads(result.keywords) if result.keywords else [],
                'source': result.source_url or 'Internal Knowledge Base'
            })
        
        return jsonify({
            'success': True,
            'results': search_results,
            'total_found': len(search_results)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
