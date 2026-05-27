from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field
from datetime import datetime, timezone
import asyncio, structlog, numpy as np

logger = structlog.get_logger()

@dataclass
class StreamStats:
    frames_processed: int = 0
    frames_dropped: int = 0
    errors: int = 0
    latency_ms: float = 0.0

class StreamProcessor:
    def __init__(self, max_streams: int = 100, frame_skip: int = 2):
        self._streams: Dict[str, Dict] = {}
        self._stats: Dict[str, StreamStats] = {}
        self._callbacks: Dict[str, List[Callable]] = {}
        self._max_streams = max_streams
        self._frame_skip = frame_skip

    async def add_stream(self, stream_id: str, url: str, config: Dict = None):
        if len(self._streams) >= self._max_streams:
            raise ValueError("Max streams reached")
        self._streams[stream_id] = {"url": url, "config": config or {}, "active": True}
        self._stats[stream_id] = StreamStats()
        logger.info("stream_added", stream_id=stream_id)

    async def remove_stream(self, stream_id: str):
        self._streams.pop(stream_id, None)
        logger.info("stream_removed", stream_id=stream_id)

    def register_callback(self, stream_id: str, callback: Callable):
        if stream_id not in self._callbacks: self._callbacks[stream_id] = []
        self._callbacks[stream_id].append(callback)

    async def process_frame(self, stream_id: str, frame: np.ndarray, frame_number: int):
        stats = self._stats.get(stream_id)
        if stats is None: return
        if frame_number % self._frame_skip != 0:
            stats.frames_dropped += 1
            return
        for cb in self._callbacks.get(stream_id, []):
            try: await cb(stream_id, frame, frame_number)
            except Exception as e: stats.errors += 1
        stats.frames_processed += 1

    def get_stats(self, stream_id: str) -> Optional[Dict]:
        s = self._stats.get(stream_id)
        return {"frames_processed": s.frames_processed, "errors": s.errors} if s else None

stream_processor = StreamProcessor()
