#!/bin/bash
# Quick start script for Perplexity AI API Server

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Perplexity AI - OpenAI Compatible API Server                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
python3 -c "import fastapi, uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required dependencies..."
    pip install -r requirements.txt
fi

# Set default values
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
BACKEND="${PERPLEXITY_BACKEND:-perplexity}"

echo ""
echo "Starting API server..."
echo "  Host: $HOST"
echo "  Port: $PORT"
echo "  Backend: $BACKEND"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

# Start the server
python3 api_server.py --host "$HOST" --port "$PORT" --backend "$BACKEND"
