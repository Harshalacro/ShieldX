#!/bin/bash

# Cloud Run / Render injects the PORT environment variable. We default to 8000.
PORT=${PORT:-8000}

echo "Starting FastAPI on port $PORT..."
# Start FastAPI as the MAIN process receiving traffic
uvicorn src.api:app --host 0.0.0.0 --port $PORT
