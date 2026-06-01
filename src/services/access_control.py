from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from enum import Enum
import structlog

logger = structlog.get_logger()

class AccessLevel(str, Enum):
    PUBLIC = "public"
    RESTRICTED = "restricted"
    HIGH_SECURITY = "high_security"
    TOP_SECRET = "top_secret"

class AccessDecision(str, Enum):
    GRANTED = "granted"
    DENIED = "denied"

class AccessControlService:
    def __init__(self):
        self._personnel: Dict[str, Dict] = {}
        self._access_log: List[Dict] = []

    def register_person(self, person_id: str, name: str, access_level: AccessLevel, zones: List[str] = None):
        self._personnel[person_id] = {"name": name, "access_level": access_level, "zones": zones or []}

    async def check_access(self, person_id: str, zone_id: str) -> AccessDecision:
        person = self._personnel.get(person_id)
        if not person:
            self._access_log.append({"person_id": person_id, "zone": zone_id, "decision": "denied", "reason": "Unknown"})
            return AccessDecision.DENIED
        if zone_id in person.get("zones", []):
            self._access_log.append({"person_id": person_id, "zone": zone_id, "decision": "granted"})
            return AccessDecision.GRANTED
        self._access_log.append({"person_id": person_id, "zone": zone_id, "decision": "denied", "reason": "No zone access"})
        return AccessDecision.DENIED

access_control_service = AccessControlService()
