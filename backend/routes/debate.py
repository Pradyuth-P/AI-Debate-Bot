from fastapi import APIRouter, HTTPException, Depends
from models.schemas import (
    StartDebateRequest,
    StartDebateResponse,
    DebateMessageRequest,
    DebateMessageResponse,
    SessionSummaryResponse,
)
from services import get_debate_engine, DebateEngine

router = APIRouter()


def get_engine() -> DebateEngine:
    return get_debate_engine()


@router.post("/start", response_model=StartDebateResponse, status_code=201)
async def start_debate(
    request: StartDebateRequest,
    engine: DebateEngine = Depends(get_engine),
):
    """
    Start a new debate session.

    - **topic**: The debate topic (5-500 characters)
    - **side**: Which side the AI will argue - FOR or AGAINST
    """
    try:
        result = await engine.start_debate(
            topic=request.topic,
            side=request.side,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=f"AI service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/message", response_model=DebateMessageResponse)
async def send_argument(
    request: DebateMessageRequest,
    engine: DebateEngine = Depends(get_engine),
):
    """
    Send a user argument and receive an AI counter-argument.

    - **session_id**: The active debate session ID
    - **user_argument**: The user's debate argument (1-2000 characters)
    """
    try:
        result = await engine.process_argument(
            session_id=request.session_id,
            user_argument=request.user_argument,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=f"AI service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/session/{session_id}", response_model=SessionSummaryResponse)
async def get_session_summary(
    session_id: str,
    engine: DebateEngine = Depends(get_engine),
):
    """Get a summary of the debate session including full conversation history."""
    try:
        result = await engine.get_session_summary(session_id=session_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/session/{session_id}")
async def end_session(
    session_id: str,
    engine: DebateEngine = Depends(get_engine),
):
    """End a debate session and clean up resources."""
    success = engine.end_session(session_id=session_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    return {"message": "Session ended successfully", "session_id": session_id}
