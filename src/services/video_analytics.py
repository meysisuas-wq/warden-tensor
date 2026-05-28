from typing import Dict, Any, List
from datetime import datetime, timezone
import numpy as np, structlog
from src.detection.object_detector import object_detector
from src.detection.motion_detector import motion_detector
from src.alerts.manager import alert_manager

logger = structlog.get_logger()

class VideoAnalyticsService:
    async def process_frame(self, stream_id: str, frame: np.ndarray, frame_number: int) -> Dict[str, Any]:
        results = {"stream_id": stream_id, "frame_number": frame_number,
                   "detections": [], "motion": [], "alerts": []}

        detections = await object_detector.detect(frame)
        for det in detections:
            results["detections"].append({"label": det.label, "confidence": det.confidence, "bbox": det.bbox})
            if object_detector.should_alert(det):
                alert = await alert_manager.create_alert(alert_type="object_detected",
                    level="warning" if det.confidence > 0.9 else "info",
                    title=f"Detected: {det.label}", camera_id=stream_id, confidence=det.confidence)
                if alert: results["alerts"].append(alert)

        motion = motion_detector.detect(frame)
        for r in motion:
            results["motion"].append({"x": r.x, "y": r.y, "width": r.width, "height": r.height})

        return results

video_analytics_service = VideoAnalyticsService()
