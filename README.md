# WardenTensor

### Next-Generation Security Surveillance & Threat Detection

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![ROCm](https://img.shields.io/badge/AMD-ROCm-red.svg)](https://rocm.docs.amd.com/)

WardenTensor processes multi-stream video, network telemetry, and anomaly patterns
simultaneously, identifying threats before they escalate. From perimeter defense to
cyber monitoring — always watching, always learning.

## Key Capabilities

- **Multi-Stream Video** — Process 100+ camera feeds simultaneously
- **Tensor Inference** — GPU-accelerated threat classification via ROCm
- **Network Monitoring** — Real-time traffic anomaly detection
- **Facial Recognition** — Authorized personnel identification
- **License Plate Recognition** — Vehicle access control
- **Object Detection** — Unattended baggage, weapons, intrusions
- **Instant Alerts** — Sub-second threat notification
- **Forensic Analysis** — Event reconstruction and timeline

## Architecture

```
┌─────────────────────────────────────────────────┐
│              Data Sources                         │
│    (Cameras / Network Taps / Sensors / Logs)      │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│         Stream Processing Engine                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐    │
│  │Video     │ │Network   │ │Log           │    │
│  │Decoder   │ │Analyzer  │ │Processor     │    │
│  └──────────┘ └──────────┘ └──────────────┘    │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│       Tensor Inference Engine (ROCm)              │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐    │
│  │Object    │ │Face      │ │Anomaly       │    │
│  │Detection │ │Recognition│ │Detection    │    │
│  └──────────┘ └──────────┘ └──────────────┘    │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│           Command Center                          │
│    (Dashboard / Alerts / Forensics / Reports)     │
└─────────────────────────────────────────────────┘
```

## Quick Start

```bash
git clone https://github.com/meysisuas-wq/warden-tensor.git
cd warden-tensor
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn src.main:app --host 0.0.0.0 --port 8002
```

## Project Structure

```
warden-tensor/
├── src/
│   ├── api/          # REST + WebSocket API
│   ├── video/        # Video stream processing
│   ├── network/      # Network traffic analysis
│   ├── detection/    # Object/face/plate detection
│   ├── alerts/       # Alert management
│   ├── forensics/    # Event reconstruction
│   ├── services/     # Business services
│   └── utils/        # Utilities
├── configs/          # Configuration presets
├── docs/             # Documentation
├── scripts/          # Deployment scripts
├── tests/            # Test suite
└── docker-compose.yml
```

## Testing
```bash
pytest
pytest --cov=src --cov-report=html
```

## Documentation
- [Architecture](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Detection Models](docs/DETECTION.md)

## License
MIT License

---
*WardenTensor — Always Watching, Always Learning*
