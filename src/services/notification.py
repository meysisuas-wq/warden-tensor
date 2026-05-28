from typing import Dict, Any, List
import structlog

logger = structlog.get_logger()

class NotificationService:
    def __init__(self):
        self._channels = {}

    def register_channel(self, name: str, handler):
        self._channels[name] = handler

    async def send_alert(self, alert: Dict[str, Any], channels: List[str] = None):
        if channels is None: channels = ["webhook", "email"]
        for ch in channels:
            handler = self._channels.get(ch)
            if handler:
                try:
                    await handler(alert)
                    logger.info("notification_sent", channel=ch, alert_id=alert.get("id"))
                except Exception as e:
                    logger.error("notification_failed", channel=ch, error=str(e))

notification_service = NotificationService()
