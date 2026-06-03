#!/bin/bash
set -euo pipefail
echo "Seeding WardenTensor database..."
python src/db/seeds.py
echo "Database seeded!"
