import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os
from pathlib import Path
import logging
from ..config import config_manager

logger = logging.getLogger(__name__)

class SessionService:
    """Service for managing counseling sessions"""
    
    def __init__(self):
        self.active_sessions: Dict[str, Dict] = {}
        self.conversation_dir = Path("./conversations")
        self.conversation_dir.mkdir(exist_ok=True)
    
    def create_session(self, user_id: str, prompt_config: str, model_config: str) -> str:
        """Create a new counseling session"""
        session_id = str(uuid.uuid4())
        
        config = config_manager.get_config()
        
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "prompt_config": prompt_config,
            "model_config": model_config,
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "messages": [],
            "status": "active",
            "evaluation_scores": []
        }
        
        self.active_sessions[session_id] = session_data
        logger.info(f"Created new session {session_id} for user {user_id}")
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data"""
        return self.active_sessions.get(session_id)
    
    def add_message(self, session_id: str, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to the session"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.active_sessions[session_id]["messages"].append(message)
        self.active_sessions[session_id]["last_activity"] = datetime.now().isoformat()
        
        config = config_manager.get_config()
        if config.session.save_conversations:
            self._save_session(session_id)
    
    def get_messages(self, session_id: str) -> List[Dict]:
        """Get all messages for a session"""
        session = self.get_session(session_id)
        if not session:
            return []
        return session["messages"]
    
    def end_session(self, session_id: str):
        """End a counseling session"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id]["status"] = "completed"
            self.active_sessions[session_id]["ended_at"] = datetime.now().isoformat()
            
            self._save_session(session_id)
            
            del self.active_sessions[session_id]
            
            logger.info(f"Ended session {session_id}")
    
    def _save_session(self, session_id: str):
        """Save session data to file"""
        try:
            session_data = self.active_sessions[session_id]
            file_path = self.conversation_dir / f"{session_id}.json"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save session {session_id}: {e}")
    
    def load_session(self, session_id: str) -> Optional[Dict]:
        """Load session data from file"""
        try:
            file_path = self.conversation_dir / f"{session_id}.json"
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load session {session_id}: {e}")
        return None
    
    def get_user_sessions(self, user_id: str) -> List[Dict]:
        """Get all sessions for a user"""
        sessions = []
        
        for session in self.active_sessions.values():
            if session["user_id"] == user_id:
                sessions.append(session)
        
        for file_path in self.conversation_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                    if session_data.get("user_id") == user_id:
                        sessions.append(session_data)
            except Exception as e:
                logger.error(f"Failed to load session file {file_path}: {e}")
        
        return sorted(sessions, key=lambda x: x["created_at"], reverse=True)
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        config = config_manager.get_config()
        max_duration = config.session.max_duration
        cutoff_time = datetime.now() - timedelta(seconds=max_duration)
        
        expired_sessions = []
        for session_id, session_data in self.active_sessions.items():
            last_activity = datetime.fromisoformat(session_data["last_activity"])
            if last_activity < cutoff_time:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.end_session(session_id)
            logger.info(f"Cleaned up expired session {session_id}")

session_service = SessionService()
