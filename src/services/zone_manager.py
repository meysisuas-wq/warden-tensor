from typing import Dict, Any, List, Optional
import structlog

logger = structlog.get_logger()

DEFAULT_ZONES = {
    "entrance": {"priority": "high", "description": "Building entry points"},
    "parking": {"priority": "medium", "description": "Vehicle areas"},
    "perimeter": {"priority": "high", "description": "Boundary fences"},
    "restricted": {"priority": "critical", "description": "Server rooms, vaults"},
    "lobby": {"priority": "medium", "description": "Public areas"},
}

class ZoneManager:
    def __init__(self):
        self._zones: Dict[str, Dict] = DEFAULT_ZONES.copy()
        self._zone_cameras: Dict[str, List[str]] = {}

    def register_zone(self, zone_id: str, config: Dict):
        self._zones[zone_id] = config

    def add_camera_to_zone(self, zone_id: str, camera_id: str):
        if zone_id not in self._zone_cameras: self._zone_cameras[zone_id] = []
        if camera_id not in self._zone_cameras[zone_id]:
            self._zone_cameras[zone_id].append(camera_id)

    def get_zone_status(self) -> List[Dict]:
        return [{"zone": z, "priority": c.get("priority"), "camera_count": len(self._zone_cameras.get(z, [])),
                 "status": "covered" if self._zone_cameras.get(z) else "uncovered"}
                for z, c in self._zones.items()]

zone_manager = ZoneManager()
