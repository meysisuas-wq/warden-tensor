#!/bin/bash
set -euo pipefail
echo "Starting WardenTensor deployment..."
command -v docker >/dev/null 2>&1 || { echo "Docker is required"; exit 1; }
echo "Building containers..."
docker-compose build
echo "Starting database..."
docker-compose up -d postgres redis
sleep 5
echo "Starting services..."
docker-compose up -d
echo "Deployment complete! API: http://localhost:8002"
