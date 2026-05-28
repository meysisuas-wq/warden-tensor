from typing import Dict, Any, List, Optional
from uuid import UUID
import structlog
from src.models.camera import Camera, CameraStatus

logger = structlog.get_logger()

class CameraService:
    async def register_camera(self, db, data: dict) -> Camera:
        camera = Camera(name=data["name"], camera_id=data["camera_id"], location=data["location"],
                        zone=data.get("zone"), stream_url=data["stream_url"],
                        resolution_width=data.get("resolution_width", 1920),
                        resolution_height=data.get("resolution_height", 1080),
                        enabled_detectors=data.get("enabled_detectors", ["object", "motion"]))
        db.add(camera)
        await db.flush()
        logger.info("camera_registered", camera_id=camera.camera_id)
        return camera

    async def get_camera(self, db, camera_id: UUID) -> Optional[Camera]:
        return await db.get(Camera, camera_id)

    async def list_cameras(self, db, zone: Optional[str] = None) -> List[Camera]:
        from sqlalchemy import select
        q = select(Camera)
        if zone: q = q.where(Camera.zone == zone)
        result = await db.execute(q)
        return result.scalars().all()

camera_service = CameraService()
