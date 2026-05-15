from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from routes.debate import router as debate_router
from routes.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 AI Debate Bot Backend starting up...")
    yield
    print("🛑 AI Debate Bot Backend shutting down...")


app = FastAPI(
    title="AI Debate Bot API",
    description="Production-ready AI Debate Bot powered by OpenAI",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(debate_router, prefix="/api/debate", tags=["debate"])
app.include_router(health_router, prefix="/api", tags=["health"])


@app.get("/")
async def root():
    return {
        "message": "AI Debate Bot API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
