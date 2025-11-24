"""
Custom Flask-Session interface for ChromaDB
"""

from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict
from datetime import datetime, timedelta
import pickle
import uuid
from typing import Optional


class ChromaSession(CallbackDict, SessionMixin):
    """Session object for ChromaDB storage"""
    
    def __init__(self, initial=None, sid=None, permanent=None):
        def on_update(self):
            self.modified = True
        
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.permanent = permanent
        self.modified = False


class ChromaSessionInterface(SessionInterface):
    """Session interface for storing sessions in ChromaDB"""
    
    def __init__(self, session_ops):
        self.session_ops = session_ops
    
    def generate_sid(self):
        """Generate a unique session ID"""
        return str(uuid.uuid4())
    
    def get_expiration_time(self, app, session):
        """Get session expiration time"""
        if session.permanent:
            return datetime.now() + app.permanent_session_lifetime
        return datetime.now() + timedelta(days=1)
    
    def open_session(self, app, request):
        """Open a session from ChromaDB"""
        sid = request.cookies.get(app.config['SESSION_COOKIE_NAME'])
        
        if not sid:
            sid = self.generate_sid()
            return ChromaSession(sid=sid, permanent=False)
        
        # Try to load session from ChromaDB
        try:
            session_data = self.session_ops.get_session(sid)
            
            if session_data:
                # Check if expired
                expiry = datetime.fromisoformat(session_data['expiration'])
                if expiry > datetime.now():
                    # Deserialize session data
                    data_hex = session_data.get('data', '')
                    if data_hex:
                        # Convert hex string back to bytes
                        data_bytes = bytes.fromhex(data_hex)
                        data = pickle.loads(data_bytes)
                        return ChromaSession(data, sid=sid, permanent=True)
        except Exception as e:
            print(f"Error loading session: {e}")
        
        # Create new session if not found or expired
        return ChromaSession(sid=sid, permanent=False)
    
    def save_session(self, app, session, response):
        """Save session to ChromaDB"""
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        
        if not session:
            # Delete session if empty
            if session.modified:
                self.session_ops.delete_session(session.sid)
                response.delete_cookie(
                    app.config['SESSION_COOKIE_NAME'],
                    domain=domain,
                    path=path
                )
            return
        
        # Set cookie
        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        samesite = self.get_cookie_samesite(app)
        expires = self.get_expiration_time(app, session)
        
        # Serialize session data
        data = pickle.dumps(dict(session))
        
        # Save to ChromaDB
        try:
            # Check if session exists
            existing = self.session_ops.get_session(session.sid)
            
            if existing:
                # Update existing session
                self.session_ops.delete_session(session.sid)
            
            # Create new session entry
            session_doc = {
                'id': session.sid,
                'user_id': session.get('user_id', ''),
                'created_at': datetime.now().isoformat(),
                'expiration': expires.isoformat(),
                'data': data.hex()  # Store as hex string
            }
            
            self.session_ops.collection.add(
                ids=[session.sid],
                documents=[session.get('user_id', 'anonymous')],
                metadatas=[session_doc]
            )
            
        except Exception as e:
            print(f"Error saving session: {e}")
        
        # Set cookie in response
        response.set_cookie(
            app.config['SESSION_COOKIE_NAME'],
            session.sid,
            expires=expires,
            httponly=httponly,
            domain=domain,
            path=path,
            secure=secure,
            samesite=samesite
        )
