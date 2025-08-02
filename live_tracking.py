import json
import uuid
from datetime import datetime, timedelta
from flask import request, session
from flask_socketio import emit, join_room, leave_room
from app import db
from models import UserSession, User, Project, ProjectMember
import logging

class LiveUserTracker:
    """Track live users on projects for real-time collaboration"""
    
    def __init__(self, socketio):
        self.socketio = socketio
        self.active_sessions = {}  # session_id: user_data
        self.project_rooms = {}    # project_id: [session_ids]
        
    def start_user_session(self, user_id, project_id=None):
        """Start tracking a user session"""
        try:
            session_id = str(uuid.uuid4())
            
            # Get user info
            user = User.query.get(user_id)
            if not user:
                return None
            
            # Create session record
            user_session = UserSession(
                user_id=user_id,
                project_id=project_id,
                session_id=session_id,
                ip_address=request.environ.get('REMOTE_ADDR', ''),
                user_agent=request.environ.get('HTTP_USER_AGENT', '')
            )
            
            db.session.add(user_session)
            db.session.commit()
            
            # Store in memory for quick access
            self.active_sessions[session_id] = {
                'user_id': user_id,
                'username': user.username,
                'email': user.email,
                'project_id': project_id,
                'last_activity': datetime.utcnow(),
                'current_page': '/',
                'is_typing': False,
                'cursor_position': None
            }
            
            # Add to project room if applicable
            if project_id:
                if project_id not in self.project_rooms:
                    self.project_rooms[project_id] = []
                self.project_rooms[project_id].append(session_id)
                
                # Notify other users in the project
                self.broadcast_user_joined(project_id, user.username, session_id)
            
            logging.info(f"Started session for user {user.username} (ID: {user_id})")
            return session_id
            
        except Exception as e:
            logging.error(f"Error starting user session: {e}")
            db.session.rollback()
            return None
    
    def end_user_session(self, session_id):
        """End a user session"""
        try:
            if session_id not in self.active_sessions:
                return False
            
            session_data = self.active_sessions[session_id]
            project_id = session_data.get('project_id')
            username = session_data.get('username')
            
            # Update database
            user_session = UserSession.query.filter_by(session_id=session_id).first()
            if user_session:
                user_session.is_active = False
                db.session.commit()
            
            # Remove from memory
            del self.active_sessions[session_id]
            
            # Remove from project room
            if project_id and project_id in self.project_rooms:
                if session_id in self.project_rooms[project_id]:
                    self.project_rooms[project_id].remove(session_id)
                
                # Notify other users
                self.broadcast_user_left(project_id, username, session_id)
            
            logging.info(f"Ended session {session_id} for user {username}")
            return True
            
        except Exception as e:
            logging.error(f"Error ending user session: {e}")
            return False
    
    def update_user_activity(self, session_id, page_url=None, activity_data=None):
        """Update user activity information"""
        try:
            if session_id not in self.active_sessions:
                return False
            
            # Update memory
            self.active_sessions[session_id]['last_activity'] = datetime.utcnow()
            
            if page_url:
                self.active_sessions[session_id]['current_page'] = page_url
            
            if activity_data:
                self.active_sessions[session_id].update(activity_data)
            
            # Update database
            user_session = UserSession.query.filter_by(session_id=session_id).first()
            if user_session:
                user_session.last_activity = datetime.utcnow()
                if page_url:
                    user_session.current_page = page_url
                db.session.commit()
            
            # Broadcast activity to project members
            session_data = self.active_sessions[session_id]
            project_id = session_data.get('project_id')
            
            if project_id:
                self.broadcast_user_activity(project_id, session_id, activity_data)
            
            return True
            
        except Exception as e:
            logging.error(f"Error updating user activity: {e}")
            return False
    
    def get_project_active_users(self, project_id):
        """Get list of active users in a project"""
        try:
            active_users = []
            
            if project_id in self.project_rooms:
                for session_id in self.project_rooms[project_id]:
                    if session_id in self.active_sessions:
                        session_data = self.active_sessions[session_id]
                        
                        # Check if user is still active (last activity within 5 minutes)
                        time_diff = datetime.utcnow() - session_data['last_activity']
                        if time_diff.total_seconds() < 300:  # 5 minutes
                            active_users.append({
                                'session_id': session_id,
                                'user_id': session_data['user_id'],
                                'username': session_data['username'],
                                'current_page': session_data['current_page'],
                                'last_activity': session_data['last_activity'].isoformat(),
                                'is_typing': session_data.get('is_typing', False)
                            })
                        else:
                            # Remove inactive session
                            self.end_user_session(session_id)
            
            return active_users
            
        except Exception as e:
            logging.error(f"Error getting project active users: {e}")
            return []
    
    def set_user_typing_status(self, session_id, is_typing, typing_location=None):
        """Set user typing status"""
        try:
            if session_id not in self.active_sessions:
                return False
            
            self.active_sessions[session_id]['is_typing'] = is_typing
            self.active_sessions[session_id]['last_activity'] = datetime.utcnow()
            
            if typing_location:
                self.active_sessions[session_id]['typing_location'] = typing_location
            
            # Broadcast typing status to project members
            session_data = self.active_sessions[session_id]
            project_id = session_data.get('project_id')
            
            if project_id:
                self.broadcast_typing_status(project_id, session_id, is_typing, typing_location)
            
            return True
            
        except Exception as e:
            logging.error(f"Error setting typing status: {e}")
            return False
    
    def update_cursor_position(self, session_id, x, y, element_id=None):
        """Update user cursor position for collaborative editing"""
        try:
            if session_id not in self.active_sessions:
                return False
            
            self.active_sessions[session_id]['cursor_position'] = {
                'x': x,
                'y': y,
                'element_id': element_id,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Broadcast cursor position to project members
            session_data = self.active_sessions[session_id]
            project_id = session_data.get('project_id')
            
            if project_id:
                self.socketio.emit('cursor_update', {
                    'session_id': session_id,
                    'username': session_data['username'],
                    'cursor_position': self.active_sessions[session_id]['cursor_position']
                }, room=f'project_{project_id}')
            
            return True
            
        except Exception as e:
            logging.error(f"Error updating cursor position: {e}")
            return False
    
    def broadcast_user_joined(self, project_id, username, session_id):
        """Broadcast that a user joined the project"""
        try:
            self.socketio.emit('user_joined', {
                'username': username,
                'session_id': session_id,
                'timestamp': datetime.utcnow().isoformat(),
                'active_users': self.get_project_active_users(project_id)
            }, room=f'project_{project_id}')
            
        except Exception as e:
            logging.error(f"Error broadcasting user joined: {e}")
    
    def broadcast_user_left(self, project_id, username, session_id):
        """Broadcast that a user left the project"""
        try:
            self.socketio.emit('user_left', {
                'username': username,
                'session_id': session_id,
                'timestamp': datetime.utcnow().isoformat(),
                'active_users': self.get_project_active_users(project_id)
            }, room=f'project_{project_id}')
            
        except Exception as e:
            logging.error(f"Error broadcasting user left: {e}")
    
    def broadcast_user_activity(self, project_id, session_id, activity_data):
        """Broadcast user activity to project members"""
        try:
            if session_id in self.active_sessions:
                session_data = self.active_sessions[session_id]
                
                self.socketio.emit('user_activity', {
                    'session_id': session_id,
                    'username': session_data['username'],
                    'activity': activity_data,
                    'timestamp': datetime.utcnow().isoformat()
                }, room=f'project_{project_id}')
            
        except Exception as e:
            logging.error(f"Error broadcasting user activity: {e}")
    
    def broadcast_typing_status(self, project_id, session_id, is_typing, location=None):
        """Broadcast typing status to project members"""
        try:
            if session_id in self.active_sessions:
                session_data = self.active_sessions[session_id]
                
                self.socketio.emit('typing_status', {
                    'session_id': session_id,
                    'username': session_data['username'],
                    'is_typing': is_typing,
                    'location': location,
                    'timestamp': datetime.utcnow().isoformat()
                }, room=f'project_{project_id}')
            
        except Exception as e:
            logging.error(f"Error broadcasting typing status: {e}")
    
    def cleanup_inactive_sessions(self):
        """Clean up inactive user sessions"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(minutes=10)
            inactive_sessions = []
            
            for session_id, session_data in self.active_sessions.items():
                if session_data['last_activity'] < cutoff_time:
                    inactive_sessions.append(session_id)
            
            for session_id in inactive_sessions:
                self.end_user_session(session_id)
            
            # Also clean up database
            UserSession.query.filter(
                UserSession.last_activity < cutoff_time,
                UserSession.is_active == True
            ).update({'is_active': False})
            
            db.session.commit()
            
            if inactive_sessions:
                logging.info(f"Cleaned up {len(inactive_sessions)} inactive sessions")
            
        except Exception as e:
            logging.error(f"Error cleaning up inactive sessions: {e}")
    
    def get_session_statistics(self):
        """Get session statistics"""
        try:
            stats = {
                'total_active_sessions': len(self.active_sessions),
                'projects_with_active_users': len(self.project_rooms),
                'sessions_by_project': {}
            }
            
            for project_id, sessions in self.project_rooms.items():
                active_count = sum(1 for s in sessions if s in self.active_sessions)
                stats['sessions_by_project'][project_id] = active_count
            
            return stats
            
        except Exception as e:
            logging.error(f"Error getting session statistics: {e}")
            return {}

# Socket.IO event handlers for live tracking
def setup_live_tracking_events(socketio, live_tracker):
    """Set up Socket.IO events for live user tracking"""
    
    @socketio.on('join_project')
    def handle_join_project(data):
        """Handle user joining a project room"""
        try:
            user_id = data.get('user_id')
            project_id = data.get('project_id')
            
            if user_id and project_id:
                # Verify user has access to project
                member = ProjectMember.query.filter_by(
                    user_id=user_id,
                    project_id=project_id
                ).first()
                
                if member:
                    session_id = live_tracker.start_user_session(user_id, project_id)
                    if session_id:
                        join_room(f'project_{project_id}')
                        emit('joined_project', {
                            'session_id': session_id,
                            'project_id': project_id,
                            'active_users': live_tracker.get_project_active_users(project_id)
                        })
                else:
                    emit('error', {'message': 'Access denied to project'})
            
        except Exception as e:
            logging.error(f"Error handling join project: {e}")
            emit('error', {'message': 'Failed to join project'})
    
    @socketio.on('leave_project')
    def handle_leave_project(data):
        """Handle user leaving a project room"""
        try:
            session_id = data.get('session_id')
            project_id = data.get('project_id')
            
            if session_id and project_id:
                live_tracker.end_user_session(session_id)
                leave_room(f'project_{project_id}')
                emit('left_project', {'project_id': project_id})
            
        except Exception as e:
            logging.error(f"Error handling leave project: {e}")
    
    @socketio.on('update_activity')
    def handle_update_activity(data):
        """Handle user activity updates"""
        try:
            session_id = data.get('session_id')
            page_url = data.get('page_url')
            activity_data = data.get('activity_data', {})
            
            if session_id:
                live_tracker.update_user_activity(session_id, page_url, activity_data)
            
        except Exception as e:
            logging.error(f"Error handling activity update: {e}")
    
    @socketio.on('typing_start')
    def handle_typing_start(data):
        """Handle typing start event"""
        try:
            session_id = data.get('session_id')
            location = data.get('location')
            
            if session_id:
                live_tracker.set_user_typing_status(session_id, True, location)
            
        except Exception as e:
            logging.error(f"Error handling typing start: {e}")
    
    @socketio.on('typing_stop')
    def handle_typing_stop(data):
        """Handle typing stop event"""
        try:
            session_id = data.get('session_id')
            
            if session_id:
                live_tracker.set_user_typing_status(session_id, False)
            
        except Exception as e:
            logging.error(f"Error handling typing stop: {e}")
    
    @socketio.on('cursor_move')
    def handle_cursor_move(data):
        """Handle cursor movement for collaborative editing"""
        try:
            session_id = data.get('session_id')
            x = data.get('x')
            y = data.get('y')
            element_id = data.get('element_id')
            
            if session_id and x is not None and y is not None:
                live_tracker.update_cursor_position(session_id, x, y, element_id)
            
        except Exception as e:
            logging.error(f"Error handling cursor move: {e}")
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnect"""
        try:
            # Try to find and end session based on request context
            # This is a simplified approach - in production you'd track session mapping
            pass
            
        except Exception as e:
            logging.error(f"Error handling disconnect: {e}")

def create_live_tracker(socketio):
    """Create and configure live user tracker"""
    live_tracker = LiveUserTracker(socketio)
    setup_live_tracking_events(socketio, live_tracker)
    return live_tracker