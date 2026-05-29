import pytest
import numpy as np
from src.detection.object_detector import SECURITY_CLASSES, ALERT_CLASSES
from src.detection.motion_detector import MotionDetector
from src.detection.plate_reader import PlateReader
from src.alerts.manager import AlertManager
from src.network.anomaly_detector import NetworkAnomalyDetector

class TestObjectDetector:
    def test_security_classes(self):
        assert SECURITY_CLASSES[0] == "person"
    def test_alert_classes(self):
        assert "person" in ALERT_CLASSES

class TestMotionDetector:
    def test_first_frame(self):
        d = MotionDetector()
        assert len(d.detect(np.zeros((100,100), dtype=np.uint8))) == 0

    def test_detect_motion(self):
        d = MotionDetector(threshold=10, min_area=10)
        d.detect(np.zeros((100,100), dtype=np.uint8))
        frame = np.zeros((100,100), dtype=np.uint8)
        frame[40:60, 40:60] = 255
        assert len(d.detect(frame)) > 0

class TestPlateReader:
    def test_validate(self):
        r = PlateReader()
        assert r.validate_format("B 1234 ABC") is True
        assert r.validate_format("invalid") is False

    def test_normalize(self):
        r = PlateReader()
        assert r._normalize("b  1234  abc") == "B 1234 ABC"

    def test_authorize(self):
        r = PlateReader()
        r.register_plate("B 1234 ABC", "John")
        assert r.is_authorized("B 1234 ABC") is True
        assert r.is_authorized("Z 9999 XXX") is False

class TestAlertManager:
    def test_init(self):
        m = AlertManager()
        assert len(m._active_alerts) == 0

class TestNetworkDetector:
    def test_init(self):
        d = NetworkAnomalyDetector()
        assert len(d._traffic_counters) == 0

    @pytest.mark.asyncio
    async def test_suspicious_port(self):
        d = NetworkAnomalyDetector()
        r = await d.analyze_event({"source_ip": "192.168.1.100", "destination_ip": "10.0.0.1",
                                   "destination_port": 4444, "bytes_sent": 1000})
        assert r is not None
        assert r["anomaly_type"] == "suspicious_port"
