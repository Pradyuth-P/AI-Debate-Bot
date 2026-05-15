from fastapi import APIRouter
from services.memory_service import memory_service
import os

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring and Docker healthcheck."""
    api_key_set = bool(os.getenv("OPENAI_API_KEY"))
    return {
        "status": "healthy",
        "service": "AI Debate Bot API",
        "version": "1.0.0",
        "openai_configured": api_key_set,
        "active_sessions": memory_service.get_active_session_count(),
    }
