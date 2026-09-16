#!/bin/bash
set -e

echo "=== Stage 1: Data Engineering ==="
python code/datasets/data_processing.py

echo ""
echo "=== Stage 2: Model Engineering ==="
python code/models/train_model.py

echo ""
echo "=== Stage 3: Deployment ==="
cd code/deployment
docker compose up --build -d

echo ""
echo "=== Pipeline finished ==="
echo "API:  http://localhost:8000/docs"
echo "App:  http://localhost:8501"
