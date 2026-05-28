from typing import Dict, Any, List
from datetime import datetime, timezone
import structlog

logger = structlog.get_logger()

class EventReconstructor:
    async def build_timeline(self, detections: List[Dict], network_events: List[Dict],
                             alerts: List[Dict], start_time=None, end_time=None) -> List[Dict]:
        timeline = []
        for e in detections:
            timeline.append({"timestamp": e.get("detected_at"), "source": "detection",
                             "description": f"Detected {e.get('label')}", "severity": e.get("alert_level", "info")})
        for e in network_events:
            timeline.append({"timestamp": e.get("captured_at"), "source": "network",
                             "description": f"Network: {e.get('source_ip')} -> {e.get('destination_ip')}",
                             "severity": "warning" if e.get("is_anomaly") else "info"})
        for a in alerts:
            timeline.append({"timestamp": a.get("created_at"), "source": "alert",
                             "description": a.get("title"), "severity": a.get("level")})
        timeline.sort(key=lambda x: x.get("timestamp", datetime.min.replace(tzinfo=timezone.utc)))
        return timeline

    async def correlate_events(self, events: List[Dict], time_window: int = 300) -> List[List[Dict]]:
        if not events: return []
        clusters, current = [], [events[0]]
        for i in range(1, len(events)):
            prev_t, curr_t = events[i-1].get("timestamp"), events[i].get("timestamp")
            if prev_t and curr_t and abs((curr_t - prev_t).total_seconds()) <= time_window:
                current.append(events[i])
            else:
                clusters.append(current)
                current = [events[i]]
        clusters.append(current)
        return clusters

event_reconstructor = EventReconstructor()
