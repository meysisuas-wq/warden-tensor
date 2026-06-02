from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from enum import Enum
import structlog

logger = structlog.get_logger()

class EventType(str, Enum):
    DETECTION = "detection"
    ALERT = "alert"
    INCIDENT = "incident"
    CAMERA_STATUS = "camera_status"

class Broadcaster:
    def __init__(self):
        self._history: List[Dict] = []

    async def broadcast(self, event_type: EventType, data: Dict[str, Any]):
        event = {"type": event_type.value, "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
        self._history.append(event)
        if len(self._history) > 1000:
            self._history = self._history[-500:]

    def get_recent(self, event_type: Optional[EventType] = None, limit: int = 50) -> List[Dict]:
        events = self._history
        if event_type: events = [e for e in events if e["type"] == event_type.value]
        return events[-limit:]

broadcaster = Broadcaster()
