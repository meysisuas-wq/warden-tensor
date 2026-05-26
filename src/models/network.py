from sqlalchemy import Column, String, Float, Integer, DateTime, BigInteger, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime, timezone
from src.db.database import Base

class NetworkEvent(Base):
    __tablename__ = "network_events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_ip = Column(String(45), nullable=False, index=True)
    destination_ip = Column(String(45), nullable=False, index=True)
    source_port = Column(Integer, nullable=True)
    destination_port = Column(Integer, nullable=True)
    protocol = Column(String(10), nullable=False)
    bytes_sent = Column(BigInteger, default=0)
    bytes_received = Column(BigInteger, default=0)
    duration_ms = Column(Integer, nullable=True)
    is_anomaly = Column(Boolean, default=False, index=True)
    anomaly_score = Column(Float, nullable=True)
    anomaly_type = Column(String(50), nullable=True)
    metadata = Column(JSONB, default=dict)
    captured_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class ThreatIntel(Base):
    __tablename__ = "threat_intel"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    indicator_type = Column(String(50), nullable=False, index=True)
    indicator_value = Column(String(500), nullable=False, index=True)
    threat_type = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False)
    source = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
