#!/bin/bash
# Start FastAPI (Backend) on port 8000
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit (Frontend) on Railway's assigned port
streamlit run frontend.py --server.port $PORT --server.address 0.0.0.0