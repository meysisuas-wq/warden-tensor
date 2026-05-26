from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime, timezone
from src.db.database import Base

class DetectionEvent(Base):
    __tablename__ = "detection_events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    camera_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    detection_type = Column(String(50), nullable=False, index=True)
    label = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=False)
    bounding_box = Column(JSONB, nullable=True)
    tracking_id = Column(String(50), nullable=True)
    frame_number = Column(Integer, nullable=True)
    image_path = Column(String(500), nullable=True)
    zone = Column(String(100), nullable=True)
    is_alert = Column(Boolean, default=False, index=True)
    alert_level = Column(String(20), nullable=True)
    acknowledged = Column(Boolean, default=False)
    metadata = Column(JSONB, default=dict)
    detected_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
