import asyncio
from datetime import datetime, timezone
from src.db.database import init_db, async_session
from src.models.camera import Camera, CameraStatus

async def seed():
    await init_db()
    async with async_session() as db:
        cameras = [
            Camera(name="Main Entrance", camera_id="CAM-001", location="Building A - Main Entrance",
                   zone="entrance", stream_url="rtsp://192.168.1.101:554/stream1", status=CameraStatus.ONLINE),
            Camera(name="Parking Lot", camera_id="CAM-002", location="Parking Area",
                   zone="parking", stream_url="rtsp://192.168.1.102:554/stream1", status=CameraStatus.ONLINE),
            Camera(name="Server Room", camera_id="CAM-003", location="Building B - Server Room",
                   zone="restricted", stream_url="rtsp://192.168.1.103:554/stream1", status=CameraStatus.ONLINE),
            Camera(name="Perimeter North", camera_id="CAM-004", location="North Fence",
                   zone="perimeter", stream_url="rtsp://192.168.1.104:554/stream1", status=CameraStatus.ONLINE),
            Camera(name="Lobby", camera_id="CAM-005", location="Main Lobby",
                   zone="lobby", stream_url="rtsp://192.168.1.105:554/stream1", status=CameraStatus.ONLINE),
        ]
        db.add_all(cameras)
        await db.commit()
        print(f"Seeded {len(cameras)} cameras!")

if __name__ == "__main__":
    asyncio.run(seed())
