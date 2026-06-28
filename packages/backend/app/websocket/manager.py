"""
WebSocket Manager — Real-time agent activity streaming.

Clients subscribe to a workflow_run_id and receive live updates
as agents execute, approval gates open, and results are generated.
"""
from collections import defaultdict
from typing import Any
import json
import structlog
from fastapi import WebSocket

logger = structlog.get_logger()


class WebSocketManager:
    def __init__(self):
        # Maps workflow_run_id → set of connected WebSockets
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, websocket: WebSocket, run_id: str):
        await websocket.accept()
        self._connections[run_id].add(websocket)
        logger.info("ws_connected", run_id=run_id, total=len(self._connections[run_id]))

    def disconnect(self, websocket: WebSocket, run_id: str):
        self._connections[run_id].discard(websocket)
        if not self._connections[run_id]:
            del self._connections[run_id]
        logger.info("ws_disconnected", run_id=run_id)

    async def broadcast_to_run(self, run_id: str, data: dict[str, Any]):
        """Send a message to all clients watching a workflow run."""
        sockets = self._connections.get(run_id, set()).copy()
        dead = set()

        for ws in sockets:
            try:
                await ws.send_text(json.dumps(data))
            except Exception:
                dead.add(ws)

        for ws in dead:
            self._connections[run_id].discard(ws)

    async def send_stream_token(self, run_id: str, token: str, agent: str):
        """Stream individual tokens from agent output."""
        await self.broadcast_to_run(run_id, {
            "type": "stream_token",
            "agent": agent,
            "token": token,
        })

    def active_runs(self) -> list[str]:
        return list(self._connections.keys())


ws_manager = WebSocketManager()
