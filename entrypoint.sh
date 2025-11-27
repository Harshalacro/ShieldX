#!/bin/bash

# Start FastAPI in the background
# We bind to 127.0.0.1 so it's accessible internally but NOT exposed to Render
uvicorn src.api:app --host 127.0.0.1 --port 8000 &

# Wait for API to start (optional but good practice)
sleep 5

# Start Streamlit in the foreground
# Cloud Run injects the PORT environment variable. We default to 8501 if not set.
PORT=${PORT:-8501}

echo "Starting Streamlit on port $PORT..."
streamlit run dashboard/app.py --server.port $PORT --server.address 0.0.0.0
