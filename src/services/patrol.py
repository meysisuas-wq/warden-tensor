from typing import Dict, Any, List
from datetime import datetime, timezone
import structlog

logger = structlog.get_logger()

class PatrolService:
    def __init__(self):
        self._routes: Dict[str, Dict] = {}
        self._active_patrols: Dict[str, Dict] = {}
        self._patrol_log: List[Dict] = []

    def create_route(self, route_id: str, name: str, checkpoints: List[Dict], interval: int = 60):
        self._routes[route_id] = {"name": name, "checkpoints": checkpoints, "interval": interval}

    def start_patrol(self, route_id: str, guard_id: str) -> str:
        patrol_id = f"PAT-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        self._active_patrols[patrol_id] = {"route_id": route_id, "guard_id": guard_id,
                                           "started_at": datetime.now(timezone.utc), "checkpoints": []}
        return patrol_id

    def checkpoint_reached(self, patrol_id: str, index: int):
        p = self._active_patrols.get(patrol_id)
        if p: p["checkpoints"].append({"index": index, "time": datetime.now(timezone.utc).isoformat()})

    def complete_patrol(self, patrol_id: str):
        p = self._active_patrols.pop(patrol_id, None)
        if p:
            p["completed_at"] = datetime.now(timezone.utc)
            self._patrol_log.append(p)

    def get_active_patrols(self) -> List[Dict]:
        return list(self._active_patrols.values())

patrol_service = PatrolService()
