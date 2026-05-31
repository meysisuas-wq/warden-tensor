from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import structlog

logger = structlog.get_logger()

class ThreatIntelligence:
    def __init__(self):
        self._indicators: Dict[str, Dict] = {}

    async def load_indicators(self, indicators: List[Dict]):
        for ind in indicators:
            self._indicators[f"{ind['type']}:{ind['value']}"] = ind
        logger.info("indicators_loaded", count=len(indicators))

    async def check_ip(self, ip: str) -> Optional[Dict]:
        return self._indicators.get(f"ip:{ip}")

    async def add_indicator(self, indicator_type: str, value: str, threat_type: str, severity: str):
        self._indicators[f"{indicator_type}:{value}"] = {
            "type": indicator_type, "value": value, "threat_type": threat_type,
            "severity": severity, "added_at": datetime.now(timezone.utc).isoformat()}

    def get_stats(self) -> Dict:
        return {"total_indicators": len(self._indicators)}

threat_intelligence = ThreatIntelligence()
