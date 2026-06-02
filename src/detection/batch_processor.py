from typing import Dict, Any, List
import numpy as np, structlog
from src.config import settings
from src.detection.object_detector import object_detector

logger = structlog.get_logger()

class BatchProcessor:
    def __init__(self, batch_size: int = None):
        self._batch_size = batch_size or settings.INFERENCE_BATCH_SIZE
        self._buffer: List[Dict] = []
        self._total_processed = 0

    async def add_frame(self, stream_id: str, frame: np.ndarray, frame_number: int):
        self._buffer.append({"stream_id": stream_id, "frame": frame, "frame_number": frame_number})
        if len(self._buffer) >= self._batch_size:
            return await self.process_batch()
        return None

    async def process_batch(self) -> List[Dict]:
        if not self._buffer: return []
        batch = self._buffer.copy()
        self._buffer.clear()
        results = []
        for item in batch:
            detections = await object_detector.detect(item["frame"])
            results.append({"stream_id": item["stream_id"], "frame_number": item["frame_number"],
                            "detections": [{"label": d.label, "confidence": d.confidence, "bbox": d.bbox} for d in detections]})
        self._total_processed += len(batch)
        return results

    def get_stats(self) -> Dict:
        return {"buffer_size": len(self._buffer), "total_processed": self._total_processed}

batch_processor = BatchProcessor()
