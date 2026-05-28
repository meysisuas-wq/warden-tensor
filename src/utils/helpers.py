from datetime import datetime, timezone
import hashlib, secrets

def generate_alert_number() -> str:
    return f"ALT-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{secrets.token_hex(4).upper()}"

def generate_incident_number() -> str:
    return f"INC-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{secrets.token_hex(4).upper()}"

def calculate_confidence_tier(confidence: float) -> str:
    if confidence >= 0.95: return "very_high"
    elif confidence >= 0.85: return "high"
    elif confidence >= 0.70: return "medium"
    elif confidence >= 0.50: return "low"
    return "very_low"

def hash_frame(frame_data: bytes) -> str:
    return hashlib.sha256(frame_data).hexdigest()
