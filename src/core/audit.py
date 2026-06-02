from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import structlog

logger = structlog.get_logger()

class AuditLogger:
    def __init__(self):
        self._log: List[Dict] = []

    async def log_action(self, action: str, actor: str, resource_type: str, resource_id: str = None, details: Dict = None):
        entry = {"timestamp": datetime.now(timezone.utc).isoformat(), "action": action,
                 "actor": actor, "resource_type": resource_type, "resource_id": resource_id, "details": details or {}}
        self._log.append(entry)
        logger.info("audit_log", **entry)

    async def get_log(self, actor: Optional[str] = None, limit: int = 100) -> List[Dict]:
        logs = self._log
        if actor: logs = [l for l in logs if l["actor"] == actor]
        return logs[-limit:]

audit_logger = AuditLogger()
