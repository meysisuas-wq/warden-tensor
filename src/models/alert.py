from sqlalchemy import Column, String, Float, DateTime, Text, Boolean, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
import uuid, enum
from datetime import datetime, timezone
from src.db.database import Base

class AlertLevel(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class AlertStatus(str, enum.Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_number = Column(String(30), unique=True, nullable=False, index=True)
    camera_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    detection_event_id = Column(UUID(as_uuid=True), nullable=True)
    alert_type = Column(String(50), nullable=False, index=True)
    level = Column(SQLEnum(AlertLevel), nullable=False, index=True)
    status = Column(SQLEnum(AlertStatus), default=AlertStatus.ACTIVE, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    zone = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=False)
    evidence_paths = Column(JSONB, default=list)
    assigned_to = Column(String(255), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_number = Column(String(30), unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="open", index=True)
    severity = Column(String(20), nullable=False)
    alert_ids = Column(ARRAY(UUID), default=list)
    zones_involved = Column(ARRAY(String), default=list)
    assigned_to = Column(String(255), nullable=True)
    timeline = Column(JSONB, default=list)
    resolution = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    closed_at = Column(DateTime(timezone=True), nullable=True)
