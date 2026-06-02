from typing import Dict, Any, List
from datetime import datetime, timezone
import structlog

logger = structlog.get_logger()

class CameraHealthChecker:
    def __init__(self):
        self._status: Dict[str, Dict] = {}

    async def update_status(self, camera_id: str, is_online: bool, fps: float = 0):
        if camera_id not in self._status:
            self._status[camera_id] = {"checks": []}
        self._status[camera_id]["checks"].append({"online": is_online, "fps": fps,
                                                    "timestamp": datetime.now(timezone.utc).isoformat()})
        if len(self._status[camera_id]["checks"]) > 100:
            self._status[camera_id]["checks"] = self._status[camera_id]["checks"][-50:]

    def get_health(self, camera_id: str) -> Dict[str, Any]:
        s = self._status.get(camera_id)
        if not s: return {"camera_id": camera_id, "status": "unknown"}
        checks = s["checks"]
        uptime = sum(1 for c in checks if c["online"]) / len(checks) * 100 if checks else 0
        return {"camera_id": camera_id, "status": "online" if checks and checks[-1]["online"] else "offline",
                "uptime_pct": round(uptime, 1)}

    def get_all(self) -> List[Dict]:
        return [self.get_health(cid) for cid in self._status]

camera_health_checker = CameraHealthChecker()
