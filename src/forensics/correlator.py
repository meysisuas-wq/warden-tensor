from typing import Dict, Any, List, Optional, Set
from datetime import datetime, timezone
from uuid import uuid4
import structlog

logger = structlog.get_logger()

class EventCorrelator:
    def __init__(self, time_window: int = 300):
        self._time_window = time_window
        self._active_incidents: Dict[str, Dict] = {}

    async def process_event(self, event: Dict[str, Any]) -> Optional[Dict]:
        for iid, incident in self._active_incidents.items():
            event_time = event.get("timestamp", datetime.now(timezone.utc))
            incident_time = incident.get("updated_at", datetime.now(timezone.utc))
            if abs((event_time - incident_time).total_seconds()) <= self._time_window:
                incident["events"].append(event)
                incident["updated_at"] = datetime.now(timezone.utc)
                return incident
        return None

    async def create_incident(self, events: List[Dict]) -> Dict:
        iid = str(uuid4())
        incident = {"id": iid, "incident_number": f"INC-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid4().hex[:6].upper()}",
                    "events": events, "status": "open", "created_at": datetime.now(timezone.utc)}
        self._active_incidents[iid] = incident
        logger.info("incident_created", id=iid, events=len(events))
        return incident

    async def close_incident(self, iid: str, resolution: str = None) -> bool:
        incident = self._active_incidents.pop(iid, None)
        if incident:
            incident["status"] = "closed"
            incident["resolution"] = resolution
            return True
        return False

    def get_active_incidents(self) -> List[Dict]:
        return list(self._active_incidents.values())

event_correlator = EventCorrelator()
