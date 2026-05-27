from typing import Dict, Any, Optional
from datetime import datetime, timezone
import structlog

logger = structlog.get_logger()

SUSPICIOUS_PORTS = {22, 23, 3389, 4444, 5555, 8080, 9001}
DDOS_THRESHOLD = 1000
PORT_SCAN_THRESHOLD = 50

class NetworkAnomalyDetector:
    def __init__(self):
        self._traffic_counters: Dict[str, Dict] = {}

    async def analyze_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        src_ip = event.get("source_ip")
        dst_port = event.get("destination_port")
        bytes_sent = event.get("bytes_sent", 0)

        if src_ip:
            if src_ip not in self._traffic_counters:
                self._traffic_counters[src_ip] = {"unique_ports": set(), "request_count": 0,
                                                   "bytes_total": 0, "last_seen": datetime.now(timezone.utc)}
            c = self._traffic_counters[src_ip]
            if dst_port: c["unique_ports"].add(dst_port)
            c["request_count"] += 1
            c["bytes_total"] += bytes_sent

            if len(c["unique_ports"]) > PORT_SCAN_THRESHOLD:
                return {"anomaly_type": "port_scan", "severity": "high", "source_ip": src_ip,
                        "unique_ports": len(c["unique_ports"]), "confidence": 0.95}
            if c["request_count"] > DDOS_THRESHOLD:
                return {"anomaly_type": "ddos", "severity": "critical", "source_ip": src_ip,
                        "request_count": c["request_count"], "confidence": 0.99}

        if dst_port in SUSPICIOUS_PORTS:
            return {"anomaly_type": "suspicious_port", "severity": "warning",
                    "destination_port": dst_port, "confidence": 0.7}
        return None

    async def get_traffic_summary(self) -> Dict[str, Any]:
        return {"unique_ips": len(self._traffic_counters),
                "total_requests": sum(c["request_count"] for c in self._traffic_counters.values())}

    async def reset_counter(self, ip: str):
        self._traffic_counters.pop(ip, None)

network_anomaly_detector = NetworkAnomalyDetector()
