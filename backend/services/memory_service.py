import uuid
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from models.schemas import DebateSide, ConversationMessage, MessageRole


class DebateSession:
    """Represents a single debate session with full conversation memory."""

    def __init__(self, session_id: str, topic: str, side: DebateSide, system_prompt: str):
        self.session_id = session_id
        self.topic = topic
        self.side = side
        self.system_prompt = system_prompt
        self.turn_number = 0
        self.created_at = datetime.utcnow()
        self.last_active = datetime.utcnow()
        self.conversation_history: List[Dict[str, str]] = []
        self.message_log: List[ConversationMessage] = []

    def add_message(self, role: str, content: str):
        """Add a message to both the OpenAI-format history and display log."""
        self.conversation_history.append({"role": role, "content": content})
        self.message_log.append(
            ConversationMessage(role=MessageRole(role), content=content)
        )
        self.last_active = datetime.utcnow()

    def get_openai_messages(self) -> List[Dict[str, str]]:
        """Get messages formatted for OpenAI API including system prompt."""
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history)
        return messages

    def increment_turn(self):
        self.turn_number += 1

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "topic": self.topic,
            "side": self.side,
            "turn_number": self.turn_number,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
            "message_count": len(self.message_log),
        }


class MemoryService:
    """In-memory conversation memory management with session TTL."""

    def __init__(self, session_ttl_hours: int = 2):
        self._sessions: Dict[str, DebateSession] = {}
        self.session_ttl = timedelta(hours=session_ttl_hours)

    def create_session(
        self, topic: str, side: DebateSide, system_prompt: str
    ) -> DebateSession:
        """Create a new debate session."""
        session_id = str(uuid.uuid4())
        session = DebateSession(
            session_id=session_id,
            topic=topic,
            side=side,
            system_prompt=system_prompt,
        )
        self._sessions[session_id] = session
        self._cleanup_expired_sessions()
        return session

    def get_session(self, session_id: str) -> Optional[DebateSession]:
        """Retrieve a session by ID."""
        session = self._sessions.get(session_id)
        if session and self._is_expired(session):
            del self._sessions[session_id]
            return None
        return session

    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def _is_expired(self, session: DebateSession) -> bool:
        return datetime.utcnow() - session.last_active > self.session_ttl

    def _cleanup_expired_sessions(self):
        """Remove expired sessions to prevent memory leaks."""
        expired = [
            sid for sid, session in self._sessions.items()
            if self._is_expired(session)
        ]
        for sid in expired:
            del self._sessions[sid]

    def get_active_session_count(self) -> int:
        self._cleanup_expired_sessions()
        return len(self._sessions)


# Singleton memory service instance
memory_service = MemoryService()
