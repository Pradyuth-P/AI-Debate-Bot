from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class DebateSide(str, Enum):
    FOR = "FOR"
    AGAINST = "AGAINST"


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationMessage(BaseModel):
    role: MessageRole
    content: str


class StartDebateRequest(BaseModel):
    topic: str = Field(..., min_length=5, max_length=500, description="The debate topic")
    side: DebateSide = Field(..., description="Which side the AI will argue: FOR or AGAINST")

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Artificial Intelligence will replace most jobs in the next decade",
                "side": "FOR",
            }
        }


class StartDebateResponse(BaseModel):
    session_id: str
    topic: str
    side: DebateSide
    opening_argument: str
    message: str = "Debate session started successfully"


class DebateMessageRequest(BaseModel):
    session_id: str = Field(..., description="The debate session ID")
    user_argument: str = Field(
        ..., min_length=1, max_length=2000, description="The user's argument"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "abc123",
                "user_argument": "AI cannot replace creative jobs that require human intuition",
            }
        }


class ArgumentAnalysis(BaseModel):
    strength: str
    key_points: List[str]
    logical_fallacies: Optional[List[str]] = None
    rating: int = Field(..., ge=1, le=10, description="Argument strength rating 1-10")


class DebateMessageResponse(BaseModel):
    session_id: str
    counter_argument: str
    analysis: ArgumentAnalysis
    turn_number: int
    topic: str
    side: DebateSide


class SessionSummaryResponse(BaseModel):
    session_id: str
    topic: str
    side: DebateSide
    total_turns: int
    conversation_history: List[ConversationMessage]
    summary: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int
