from typing import Optional, List, Dict
from collections import deque
from datetime import datetime, timezone
import numpy as np

class FrameBuffer:
    def __init__(self, capacity: int = 300, fps: int = 30):
        self._buffer: deque = deque(maxlen=capacity)
        self._capacity = capacity
        self._fps = fps
        self._frame_count = 0

    def push(self, frame: np.ndarray, metadata: Dict = None):
        self._buffer.append({"frame": frame, "frame_number": self._frame_count,
                             "timestamp": datetime.now(timezone.utc), "metadata": metadata or {}})
        self._frame_count += 1

    def get_latest(self, count: int = 1) -> List[Dict]:
        return list(self._buffer)[-count:]

    def get_last_n_seconds(self, seconds: float) -> List[Dict]:
        return list(self._buffer)[-int(seconds * self._fps):]

    @property
    def size(self) -> int:
        return len(self._buffer)

class MultiStreamBuffer:
    def __init__(self, capacity: int = 300):
        self._buffers: Dict[str, FrameBuffer] = {}
        self._capacity = capacity

    def get_or_create(self, stream_id: str, fps: int = 30) -> FrameBuffer:
        if stream_id not in self._buffers:
            self._buffers[stream_id] = FrameBuffer(self._capacity, fps)
        return self._buffers[stream_id]

    def remove(self, stream_id: str):
        self._buffers.pop(stream_id, None)

frame_buffer = FrameBuffer()
multi_stream_buffer = MultiStreamBuffer()
