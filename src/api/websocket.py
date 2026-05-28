from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Set
import structlog

logger = structlog.get_logger()
router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self._connections: Set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self._connections.add(ws)
        logger.info("ws_connected", total=len(self._connections))

    async def disconnect(self, ws: WebSocket):
        self._connections.discard(ws)

    async def broadcast(self, message: dict):
        dead = set()
        for c in self._connections:
            try: await c.send_json(message)
            except: dead.add(c)
        for c in dead: self._connections.discard(c)

manager = ConnectionManager()

@router.websocket("/ws/events")
async def events_stream(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True: await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)

@router.websocket("/ws/alerts")
async def alerts_stream(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True: await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)

async def broadcast_event(event: dict):
    await manager.broadcast({"type": "event", "data": event})

async def broadcast_alert(alert: dict):
    await manager.broadcast({"type": "alert", "data": alert})
