import pytest
from datetime import datetime, timezone, timedelta
from src.forensics.reconstructor import EventReconstructor

class TestReconstructor:
    @pytest.mark.asyncio
    async def test_build_timeline(self):
        r = EventReconstructor()
        now = datetime.now(timezone.utc)
        detections = [{"detected_at": now - timedelta(minutes=5), "label": "person", "alert_level": "info"}]
        alerts = [{"created_at": now, "title": "Alert", "level": "critical"}]
        timeline = await r.build_timeline(detections, [], alerts)
        assert len(timeline) == 2
        assert timeline[0]["source"] == "detection"

    @pytest.mark.asyncio
    async def test_correlate(self):
        r = EventReconstructor()
        now = datetime.now(timezone.utc)
        events = [{"timestamp": now}, {"timestamp": now + timedelta(seconds=30)},
                  {"timestamp": now + timedelta(minutes=10)}]
        clusters = await r.correlate_events(events, time_window=120)
        assert len(clusters) == 2
