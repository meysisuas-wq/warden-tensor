from typing import Dict, Any, List
from datetime import datetime, timezone
import json, csv, io, structlog

logger = structlog.get_logger()

class ExportService:
    async def export_json(self, data: List[Dict]) -> str:
        return json.dumps(data, indent=2, default=str)

    async def export_csv(self, data: List[Dict], fields: List[str] = None) -> str:
        if not data: return ""
        output = io.StringIO()
        if fields is None: fields = list(data[0].keys())
        writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()

    async def generate_report(self, detections: List[Dict], alerts: List[Dict]) -> Dict[str, Any]:
        types = {}
        for d in detections:
            t = d.get("detection_type", "unknown")
            types[t] = types.get(t, 0) + 1
        return {"generated_at": datetime.now(timezone.utc).isoformat(),
                "total_detections": len(detections), "total_alerts": len(alerts), "detection_types": types}

export_service = ExportService()
