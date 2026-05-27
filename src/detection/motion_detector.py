from typing import List, Optional
from dataclasses import dataclass
import numpy as np

@dataclass
class MotionRegion:
    x: int; y: int; width: int; height: int; area: int; intensity: float

class MotionDetector:
    def __init__(self, threshold: int = 25, min_area: int = 500):
        self._background: Optional[np.ndarray] = None
        self._threshold = threshold
        self._min_area = min_area

    def detect(self, frame: np.ndarray) -> List[MotionRegion]:
        if len(frame.shape) == 3:
            gray = np.mean(frame, axis=2).astype(np.uint8)
        else:
            gray = frame
        if self._background is None:
            self._background = gray.astype(np.float64)
            return []
        diff = np.abs(gray.astype(np.float64) - self._background)
        mask = (diff > self._threshold).astype(np.uint8) * 255
        regions = self._find_regions(mask)
        self._background = self._background * 0.99 + gray.astype(np.float64) * 0.01
        return regions

    def _find_regions(self, mask: np.ndarray) -> List[MotionRegion]:
        h, w = mask.shape
        visited = np.zeros_like(mask, dtype=bool)
        regions = []
        for y in range(0, h, 10):
            for x in range(0, w, 10):
                if mask[y, x] > 0 and not visited[y, x]:
                    pixels = self._flood_fill(mask, visited, x, y)
                    if len(pixels) > self._min_area // 100:
                        xs = [p[0] for p in pixels]
                        ys = [p[1] for p in pixels]
                        regions.append(MotionRegion(min(xs), min(ys), max(xs)-min(xs), max(ys)-min(ys),
                                                    len(pixels), np.mean([mask[p[1],p[0]] for p in pixels])))
        return regions

    def _flood_fill(self, mask, visited, sx, sy):
        stack = [(sx, sy)]
        pixels = []
        while stack and len(pixels) < 1000:
            x, y = stack.pop()
            if 0 <= x < mask.shape[1] and 0 <= y < mask.shape[0] and not visited[y, x] and mask[y, x] > 0:
                visited[y, x] = True
                pixels.append((x, y))
                stack.extend([(x+1,y),(x-1,y),(x,y+1),(x,y-1)])
        return pixels

motion_detector = MotionDetector()
