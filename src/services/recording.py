from typing import Dict, Any, Optional
from datetime import datetime, timezone
from pathlib import Path
import structlog

logger = structlog.get_logger()

class RecordingService:
    def __init__(self, storage_path: str = "./data/recordings"):
        self._storage_path = Path(storage_path)
        self._storage_path.mkdir(parents=True, exist_ok=True)
        self._active: Dict[str, Dict] = {}

    async def start_recording(self, camera_id: str, trigger: str, duration: int = 30) -> str:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filepath = self._storage_path / camera_id / f"{camera_id}_{ts}_{trigger}.mp4"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        self._active[camera_id] = {"filepath": str(filepath), "started_at": datetime.now(timezone.utc), "trigger": trigger}
        logger.info("recording_started", camera_id=camera_id, file=str(filepath))
        return str(filepath)

    async def stop_recording(self, camera_id: str) -> Optional[str]:
        rec = self._active.pop(camera_id, None)
        return rec["filepath"] if rec else None

    def get_storage_usage(self) -> Dict[str, Any]:
        total = sum(f.stat().st_size for f in self._storage_path.rglob("*.mp4"))
        return {"total_size_mb": round(total / (1024*1024), 2), "file_count": len(list(self._storage_path.rglob("*.mp4")))}

recording_service = RecordingService()
