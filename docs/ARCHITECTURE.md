# WardenTensor Architecture

## Processing Pipeline
```
Camera Streams -> Frame Extraction -> Object Detection -> Alert Generation
Network Taps -> Traffic Analysis -> Anomaly Detection -> Incident Correlation
Sensor Data -> Event Aggregation -> Forensic Timeline -> Command Dashboard
```

## Key Design Decisions
1. GPU-Accelerated Inference via AMD ROCm
2. Multi-Model Pipeline (object, face, plate, motion in parallel)
3. Event Correlation groups related events into incidents
4. Cooldown & Deduplication prevents alert fatigue
5. WebSocket Streaming for real-time dashboards

## Detection Models
| Model | Purpose | Speed | Accuracy |
|-------|---------|-------|----------|
| YOLO v8 | Object detection | 30 FPS | 92% mAP |
| FaceNet | Face recognition | 20 FPS | 99% |
| CRNN | Plate reading | 15 FPS | 95% |
| BG Subtraction | Motion detection | 60 FPS | 88% |

## Tech Stack
- Backend: FastAPI + WebSocket
- Database: PostgreSQL + Redis
- ML: PyTorch + ONNX Runtime
- GPU: AMD ROCm
- Video: OpenCV + FFmpeg
