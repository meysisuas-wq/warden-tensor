from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from uuid import uuid4
import structlog
from src.config import settings

logger = structlog.get_logger()

class AlertManager:
    def __init__(self):
        self._active_alerts: Dict[str, Dict] = {}
        self._cooldowns: Dict[str, datetime] = {}
        self._alert_history: List[Dict] = []
        self._handlers: List = []

    def register_handler(self, handler):
        self._handlers.append(handler)

    async def create_alert(self, alert_type: str, level: str, title: str, camera_id: str,
                           zone: str = None, confidence: float = 0.0, description: str = None) -> Optional[Dict]:
        cooldown_key = f"{alert_type}:{camera_id}:{zone}"
        if cooldown_key in self._cooldowns:
            if (datetime.now(timezone.utc) - self._cooldowns[cooldown_key]).seconds < settings.ALERT_COOLDOWN_SECONDS:
                return None

        alert = {"id": str(uuid4()), "alert_number": f"ALT-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid4().hex[:6].upper()}",
                 "alert_type": alert_type, "level": level, "title": title, "description": description,
                 "camera_id": camera_id, "zone": zone, "confidence": confidence,
                 "status": "active", "created_at": datetime.now(timezone.utc)}

        self._active_alerts[alert["id"]] = alert
        self._alert_history.append(alert)
        self._cooldowns[cooldown_key] = datetime.now(timezone.utc)

        for h in self._handlers:
            try: await h(alert)
            except: pass

        logger.info("alert_created", id=alert["id"], type=alert_type, level=level)
        return alert

    async def acknowledge_alert(self, alert_id: str, user: str) -> bool:
        alert = self._active_alerts.get(alert_id)
        if not alert: return False
        alert["status"] = "acknowledged"
        alert["acknowledged_by"] = user
        return True

    async def resolve_alert(self, alert_id: str, notes: str = None) -> bool:
        alert = self._active_alerts.pop(alert_id, None)
        if not alert: return False
        alert["status"] = "resolved"
        return True

    def get_active_alerts(self, level: Optional[str] = None) -> List[Dict]:
        alerts = list(self._active_alerts.values())
        if level: alerts = [a for a in alerts if a["level"] == level]
        return sorted(alerts, key=lambda x: x["created_at"], reverse=True)

    def get_stats(self) -> Dict:
        active = list(self._active_alerts.values())
        return {"total_active": len(active), "critical": len([a for a in active if a["level"] == "critical"]),
                "warning": len([a for a in active if a["level"] == "warning"]),
                "total_historical": len(self._alert_history)}

alert_manager = AlertManager()
