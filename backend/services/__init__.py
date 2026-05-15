from .openai_service import OpenAIService
from .memory_service import MemoryService, memory_service
from .debate_engine import DebateEngine

# Singleton instances for dependency injection
_openai_service = None
_debate_engine = None


def get_openai_service() -> OpenAIService:
    global _openai_service
    if _openai_service is None:
        _openai_service = OpenAIService()
    return _openai_service


def get_debate_engine() -> DebateEngine:
    global _debate_engine
    if _debate_engine is None:
        _debate_engine = DebateEngine(
            openai_service=get_openai_service(),
            memory_service=memory_service,
        )
    return _debate_engine


__all__ = [
    "OpenAIService",
    "MemoryService",
    "DebateEngine",
    "memory_service",
    "get_openai_service",
    "get_debate_engine",
]
