from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
import uuid, enum
from datetime import datetime, timezone
from src.db.database import Base

class CameraStatus(str, enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"
    ERROR = "error"

class Camera(Base):
    __tablename__ = "cameras"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    camera_id = Column(String(50), unique=True, nullable=False, index=True)
    location = Column(String(500), nullable=False)
    zone = Column(String(100), nullable=True, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    stream_url = Column(String(500), nullable=False)
    status = Column(SQLEnum(CameraStatus), default=CameraStatus.OFFLINE, index=True)
    resolution_width = Column(Integer, default=1920)
    resolution_height = Column(Integer, default=1080)
    fps = Column(Integer, default=30)
    is_ptz = Column(Boolean, default=False)
    detection_zones = Column(JSONB, default=list)
    enabled_detectors = Column(ARRAY(String), default=["object", "motion"])
    last_frame_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
