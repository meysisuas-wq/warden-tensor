# WardenTensor Deployment Guide

## Quick Start
```bash
git clone https://github.com/meysisuas-wq/warden-tensor.git
cd warden-tensor
cp .env.example .env
docker-compose up -d
```

## Manual
```bash
createdb wardentensor
alembic upgrade head
gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8002
```

## GPU Setup
```bash
# AMD ROCm
sudo apt install rocm-dev
rocm-smi
# Enable: ROCM_ENABLED=true in .env
```

## Camera Integration
```bash
# Register camera
curl -X POST http://localhost:8002/api/v1/cameras \
  -H "Content-Type: application/json" \
  -d '{"name":"Entrance","camera_id":"CAM-001","location":"Main Entrance","zone":"entrance","stream_url":"rtsp://192.168.1.100:554/stream1"}'
```

## Monitoring
```bash
curl http://localhost:8002/health
docker-compose logs -f api | jq .
```

## Scaling
- Add API replicas for concurrent streams
- Redis cluster for distributed state
- Scale GPU workers independently
