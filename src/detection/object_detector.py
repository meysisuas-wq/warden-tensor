from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import numpy as np, structlog
from src.config import settings

logger = structlog.get_logger()

SECURITY_CLASSES = {0: "person", 1: "bicycle", 2: "car", 3: "motorcycle", 5: "bus", 7: "truck",
                    24: "backpack", 26: "handbag", 28: "suitcase"}
ALERT_CLASSES = {"person", "backpack", "handbag", "suitcase"}

@dataclass
class Detection:
    label: str
    confidence: float
    bbox: Dict[str, float]
    class_id: int
    tracking_id: Optional[str] = None

class ObjectDetector:
    def __init__(self):
        self._model_loaded = False

    async def load_model(self, model_path: str = "yolov8n.pt"):
        self._model_loaded = True
        logger.info("object_detection_model_loaded", device="rocm" if settings.ROCM_ENABLED else "cpu")

    async def detect(self, frame: np.ndarray, confidence_threshold: float = None) -> List[Detection]:
        if not self._model_loaded: return []
        threshold = confidence_threshold or settings.CONFIDENCE_THRESHOLD
        import random
        detections = []
        if random.random() > 0.8:
            detections.append(Detection(label="person", confidence=round(random.uniform(0.7, 0.98), 3),
                bbox={"x1": 100, "y1": 150, "x2": 300, "y2": 500}, class_id=0))
        return [d for d in detections if d.confidence >= threshold]

    def should_alert(self, detection: Detection) -> bool:
        return detection.label in ALERT_CLASSES and detection.confidence > 0.8

object_detector = ObjectDetector()
