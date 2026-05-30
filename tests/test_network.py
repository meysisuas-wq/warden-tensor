import pytest
from src.network.anomaly_detector import NetworkAnomalyDetector

class TestNetworkDetector:
    @pytest.mark.asyncio
    async def test_port_scan(self):
        d = NetworkAnomalyDetector()
        for port in range(1, 60):
            await d.analyze_event({"source_ip": "192.168.1.100", "destination_ip": "10.0.0.1",
                                   "destination_port": port, "bytes_sent": 100})
        r = await d.analyze_event({"source_ip": "192.168.1.100", "destination_ip": "10.0.0.1",
                                   "destination_port": 99, "bytes_sent": 100})
        assert r is not None
        assert r["anomaly_type"] == "port_scan"

    @pytest.mark.asyncio
    async def test_summary(self):
        d = NetworkAnomalyDetector()
        await d.analyze_event({"source_ip": "1.1.1.1", "destination_ip": "2.2.2.2",
                               "destination_port": 80, "bytes_sent": 1000})
        s = await d.get_traffic_summary()
        assert s["unique_ips"] >= 1

    @pytest.mark.asyncio
    async def test_reset(self):
        d = NetworkAnomalyDetector()
        await d.analyze_event({"source_ip": "10.0.0.1", "destination_ip": "10.0.0.2",
                               "destination_port": 80, "bytes_sent": 500})
        await d.reset_counter("10.0.0.1")
        assert (await d.get_traffic_summary())["unique_ips"] == 0
