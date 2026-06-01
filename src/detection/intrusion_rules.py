from typing import Dict, Any, List
from datetime import datetime, timezone
from dataclasses import dataclass
import structlog

logger = structlog.get_logger()

@dataclass
class IntrusionRule:
    rule_id: str
    name: str
    zone: str
    condition: str
    severity: str
    enabled: bool = True

DEFAULT_RULES = [
    IntrusionRule("IR-001", "After-hours perimeter breach", "perimeter", "person_in_zone", "critical"),
    IntrusionRule("IR-002", "Restricted zone entry", "restricted", "person_in_zone", "critical"),
    IntrusionRule("IR-003", "Loitering detection", "*", "loitering", "warning"),
    IntrusionRule("IR-004", "Line crossing", "perimeter", "line_crossing", "high"),
]

class IntrusionDetector:
    def __init__(self):
        self._rules: List[IntrusionRule] = DEFAULT_RULES.copy()

    def add_rule(self, rule: IntrusionRule):
        self._rules.append(rule)

    def evaluate(self, detection: Dict, zone: str) -> List[Dict]:
        violations = []
        for rule in self._rules:
            if not rule.enabled: continue
            if rule.zone != "*" and rule.zone != zone: continue
            if rule.condition == "person_in_zone" and detection.get("label") == "person":
                violations.append({"rule_id": rule.rule_id, "name": rule.name,
                                   "severity": rule.severity, "zone": zone})
        return violations

    def get_rules(self) -> List[Dict]:
        return [{"rule_id": r.rule_id, "name": r.name, "zone": r.zone,
                 "condition": r.condition, "severity": r.severity, "enabled": r.enabled} for r in self._rules]

intrusion_detector = IntrusionDetector()
