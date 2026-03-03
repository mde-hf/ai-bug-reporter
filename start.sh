#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_info() { echo -e "${BLUE}ℹ${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }

echo ""
echo "🚀 Starting Bug Reporter..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found. Please run ./setup.sh first"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    print_error ".env file not found. Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    print_error "Dependencies not installed. Please run ./setup.sh first"
    exit 1
fi

# Start the application
print_success "Starting application on port 5000..."
echo ""
print_info "Visit: ${BLUE}http://localhost:5000${NC}"
print_info "Press Ctrl+C to stop the server"
echo ""

python app.py
