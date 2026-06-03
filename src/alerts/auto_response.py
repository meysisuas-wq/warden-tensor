from typing import Dict, Any, List, Callable
from datetime import datetime, timezone
import asyncio, structlog

logger = structlog.get_logger()

class AutoResponseSystem:
    def __init__(self):
        self._rules: List[Dict] = []
        self._action_handlers: Dict[str, Callable] = {}
        self._executed: List[Dict] = []

    def register_action(self, name: str, handler: Callable):
        self._action_handlers[name] = handler

    def add_rule(self, alert_type: str, level: str, actions: List[str]):
        self._rules.append({"alert_type": alert_type, "level": level, "actions": actions})

    async def process_alert(self, alert: Dict[str, Any]):
        for rule in self._rules:
            if (rule["alert_type"] == "*" or rule["alert_type"] == alert.get("alert_type")) and \
               (rule["level"] == "*" or rule["level"] == alert.get("level")):
                for action in rule["actions"]:
                    handler = self._action_handlers.get(action)
                    if handler:
                        try:
                            await handler(alert)
                            self._executed.append({"action": action, "alert_id": alert.get("id"),
                                                    "executed_at": datetime.now(timezone.utc).isoformat()})
                        except Exception as e:
                            logger.error("auto_action_failed", action=action, error=str(e))

async def send_notification(alert: Dict):
    logger.info("sending_notification", alert_id=alert.get("id"))

async def record_clip(alert: Dict):
    logger.info("recording_clip", camera=alert.get("camera_id"))

auto_response = AutoResponseSystem()
auto_response.register_action("notify", send_notification)
auto_response.register_action("record", record_clip)
auto_response.add_rule("*", "critical", ["notify", "record"])
auto_response.add_rule("*", "warning", ["notify"])
auto_response.add_rule("*", "info", ["record"])
