from typing import Dict, Any
from datetime import datetime, timezone
import structlog

logger = structlog.get_logger()

class HealthMonitor:
    def __init__(self):
        self._components: Dict[str, Dict] = {}

    def register_component(self, name: str, check_fn=None):
        self._components[name] = {"check_fn": check_fn, "status": "unknown"}

    async def check_all(self) -> Dict[str, Any]:
        overall = True
        results = {}
        for name, comp in self._components.items():
            try:
                if comp["check_fn"]:
                    ok = await comp["check_fn"]()
                    comp["status"] = "healthy" if ok else "unhealthy"
                    if not ok: overall = False
                else:
                    comp["status"] = "healthy"
            except:
                comp["status"] = "error"
                overall = False
            results[name] = comp["status"]
        return {"overall": "healthy" if overall else "degraded", "components": results,
                "timestamp": datetime.now(timezone.utc).isoformat()}

health_monitor = HealthMonitor()
