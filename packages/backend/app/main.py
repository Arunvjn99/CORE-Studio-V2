"""
CORE Studio V2 — FastAPI Application Entry Point
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import structlog
from pathlib import Path

from app.core.config import settings
from app.db.base import engine, Base
from app.api.v1.endpoints import auth, projects, workflows, knowledge, artifacts
from app.websocket.manager import ws_manager
from app.core.deps import get_current_user

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    logger.info("startup", app=settings.APP_NAME, version=settings.APP_VERSION)

    # Create upload directories
    for dir_path in ["./uploads/knowledge", "./uploads/screens"]:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    # Create DB tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("database_ready")
    yield
    logger.info("shutdown")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Design Office Platform",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REST API routes
app.include_router(auth.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(workflows.router, prefix="/api/v1")
app.include_router(knowledge.router, prefix="/api/v1")
app.include_router(artifacts.router, prefix="/api/v1")


# WebSocket — real-time agent streaming
@app.websocket("/ws/workflows/{run_id}")
async def workflow_websocket(websocket: WebSocket, run_id: str):
    """
    Connect to receive live updates for a workflow run.

    Message types:
    - step_start: agent step beginning
    - stream_token: live token stream from agent
    - step_complete: agent step finished
    - approval_required: human gate opened
    - gate_decision: gate approved/rejected
    - workflow_complete: full run finished
    """
    await ws_manager.connect(websocket, run_id)
    try:
        while True:
            # Keep connection alive — clients can send ping messages
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text('{"type":"pong"}')
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, run_id)


@app.get("/api/health")
async def health():
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.get("/api/health/ready")
async def readiness():
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        return {"status": "ready"}
    except Exception as e:
        return {"status": "not_ready", "error": str(e)}
