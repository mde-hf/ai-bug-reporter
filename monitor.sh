#!/bin/bash

# Flask Auto-Monitor and Restart Script
# This script monitors the Flask server and automatically restarts it if it crashes

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo ""
echo "🔄 Flask Auto-Monitor Started"
echo "=============================="
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo -e "${RED}✗${NC} Virtual environment not found. Run ./setup.sh first"
    exit 1
fi

# Function to start Flask server
start_server() {
    echo -e "${BLUE}ℹ${NC} Starting Flask server..."
    python app.py &
    FLASK_PID=$!
    echo -e "${GREEN}✓${NC} Flask server started (PID: $FLASK_PID)"
}

# Function to check if Flask is running
is_flask_running() {
    if ps -p $FLASK_PID > /dev/null 2>&1; then
        return 0  # Running
    else
        return 1  # Not running
    fi
}

# Trap CTRL+C to gracefully shutdown
cleanup() {
    echo ""
    echo -e "${YELLOW}⚠${NC} Shutting down monitor and Flask server..."
    if [ ! -z "$FLASK_PID" ]; then
        kill $FLASK_PID 2>/dev/null
    fi
    echo -e "${GREEN}✓${NC} Cleanup complete"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Flask server initially
start_server

# Monitor loop
CHECK_INTERVAL=5  # Check every 5 seconds
RESTART_COUNT=0

echo ""
echo -e "${GREEN}✓${NC} Monitor active - Checking every ${CHECK_INTERVAL} seconds"
echo -e "${YELLOW}⚠${NC} Press CTRL+C to stop"
echo ""

while true; do
    sleep $CHECK_INTERVAL
    
    if ! is_flask_running; then
        RESTART_COUNT=$((RESTART_COUNT + 1))
        echo ""
        echo -e "${RED}✗${NC} Flask server stopped unexpectedly!"
        echo -e "${BLUE}ℹ${NC} Restart attempt #${RESTART_COUNT}"
        
        # Wait a moment before restarting
        sleep 2
        
        # Start server again
        start_server
        
        echo ""
        echo -e "${GREEN}✓${NC} Monitor resumed"
        echo ""
    fi
done
