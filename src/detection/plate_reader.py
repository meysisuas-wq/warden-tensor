from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import re, structlog

logger = structlog.get_logger()

PLATE_PATTERNS = [r'^[A-Z]{1,2}\s?\d{1,4}\s?[A-Z]{1,3}$', r'^[A-Z]{1,2}\s?\d{1,4}$']

@dataclass
class PlateResult:
    plate_number: str; confidence: float; is_registered: bool

class PlateReader:
    def __init__(self):
        self._registered_plates: Dict[str, Dict] = {}

    async def load_model(self):
        logger.info("plate_recognition_model_loaded")

    def register_plate(self, plate: str, owner: str):
        self._registered_plates[self._normalize(plate)] = {"owner": owner}

    def is_authorized(self, plate: str) -> bool:
        return self._normalize(plate) in self._registered_plates

    def _normalize(self, plate: str) -> str:
        return re.sub(r'\s+', ' ', plate.strip().upper())

    def validate_format(self, plate: str) -> bool:
        n = self._normalize(plate)
        return any(re.match(p, n) for p in PLATE_PATTERNS)

plate_reader = PlateReader()
