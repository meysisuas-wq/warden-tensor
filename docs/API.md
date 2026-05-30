# WardenTensor API Reference

## Base URL
`http://localhost:8002/api/v1`

## Endpoints

### Cameras
- POST /cameras — Register camera
- GET /cameras — List cameras
- GET /cameras/{id} — Get camera
- DELETE /cameras/{id} — Remove camera
- POST /cameras/{id}/snapshot — Take snapshot

### Detections
- GET /detections — List detections
- POST /detections/image — Analyze image

### Alerts
- GET /alerts — List alerts
- PATCH /alerts/{id} — Update alert
- POST /alerts/{id}/acknowledge — Acknowledge

### Network
- GET /network/events — Network events
- GET /network/anomalies — Anomalies

### Dashboard
- GET /dashboard — Stats

### WebSocket
- ws://localhost:8002/api/v1/ws/events — Real-time events
- ws://localhost:8002/api/v1/ws/alerts — Real-time alerts
