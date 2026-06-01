from typing import Dict
import time

class MetricsCollector:
    def __init__(self):
        self._counters: Dict[str, int] = {}
        self._gauges: Dict[str, float] = {}
        self._start_time = time.time()

    def increment(self, name: str, value: int = 1):
        self._counters[name] = self._counters.get(name, 0) + value

    def set_gauge(self, name: str, value: float):
        self._gauges[name] = value

    def get_uptime(self) -> float:
        return time.time() - self._start_time

    def export_prometheus(self) -> str:
        lines = []
        for n, v in self._counters.items(): lines.append(f"warden_tensor_{n} {v}")
        for n, v in self._gauges.items(): lines.append(f"warden_tensor_{n} {v}")
        lines.append(f"warden_tensor_uptime_seconds {self.get_uptime()}")
        return "\n".join(lines)

metrics = MetricsCollector()
