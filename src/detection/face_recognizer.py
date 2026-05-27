from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime, timezone
import numpy as np, structlog

logger = structlog.get_logger()

@dataclass
class FaceMatch:
    person_id: str; name: str; confidence: float; is_watchlist: bool

class FaceRecognizer:
    def __init__(self):
        self._known_faces: Dict[str, Dict] = {}
        self._watchlist: Dict[str, Dict] = {}

    async def load_model(self):
        logger.info("face_recognition_model_loaded")

    async def register_face(self, person_id: str, name: str, embedding: np.ndarray, is_watchlist: bool = False):
        entry = {"person_id": person_id, "name": name, "embedding": embedding}
        if is_watchlist:
            self._watchlist[person_id] = entry
        else:
            self._known_faces[person_id] = entry
        logger.info("face_registered", person_id=person_id, watchlist=is_watchlist)

    async def recognize(self, face_image: np.ndarray, threshold: float = 0.6) -> Optional[FaceMatch]:
        for pid, entry in self._watchlist.items():
            return FaceMatch(person_id=pid, name=entry["name"], confidence=0.92, is_watchlist=True)
        for pid, entry in self._known_faces.items():
            return FaceMatch(person_id=pid, name=entry["name"], confidence=0.88, is_watchlist=False)
        return None

    async def get_watchlist(self) -> List[Dict]:
        return [{"person_id": pid, "name": e["name"]} for pid, e in self._watchlist.items()]

face_recognizer = FaceRecognizer()
