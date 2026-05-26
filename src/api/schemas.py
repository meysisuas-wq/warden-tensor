from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class CameraCreate(BaseModel):
    name: str
    camera_id: str
    location: str
    zone: Optional[str] = None
    stream_url: str
    resolution_width: int = 1920
    resolution_height: int = 1080
    fps: int = 30
    is_ptz: bool = False
    enabled_detectors: List[str] = ["object", "motion"]

class CameraResponse(BaseModel):
    id: UUID; name: str; camera_id: str; location: str; zone: Optional[str]
    stream_url: str; status: str; resolution_width: int; resolution_height: int
    created_at: datetime
    class Config: from_attributes = True

class DetectionEventResponse(BaseModel):
    id: UUID; camera_id: UUID; detection_type: str; label: Optional[str]
    confidence: float; is_alert: bool; detected_at: datetime
    class Config: from_attributes = True

class AlertResponse(BaseModel):
    id: UUID; alert_number: str; camera_id: UUID; alert_type: str; level: str
    status: str; title: str; zone: Optional[str]; confidence: float; created_at: datetime
    class Config: from_attributes = True

class AlertUpdate(BaseModel):
    status: Optional[str] = None; assigned_to: Optional[str] = None
    resolution_notes: Optional[str] = None

class NetworkEventResponse(BaseModel):
    id: UUID; source_ip: str; destination_ip: str; protocol: str
    is_anomaly: bool; anomaly_score: Optional[float]; captured_at: datetime
    class Config: from_attributes = True

class DashboardStats(BaseModel):
    total_cameras: int; online_cameras: int; active_alerts: int
    critical_alerts: int; detections_today: int; network_anomalies_today: int
    system_health: str
