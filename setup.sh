#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored messages
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }
print_info() { echo -e "${BLUE}ℹ${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }

echo ""
echo "🐛 Bug Reporter - Setup Script"
echo "================================"
echo ""

# Check if Python 3 is installed
print_info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION found"

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi
print_success "pip3 found"

# Create virtual environment
print_info "Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "pip upgraded"

# Install dependencies
print_info "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
print_success "Dependencies installed"

# Setup .env file
if [ ! -f ".env" ]; then
    print_info "Creating .env file from .env.example..."
    cp .env.example .env
    print_success ".env file created"
    print_warning "Please update .env with your Jira credentials!"
    echo ""
    echo "Edit .env and add:"
    echo "  - JIRA_EMAIL=your.email@hellofresh.com"
    echo "  - JIRA_API_TOKEN=your_token_here"
    echo ""
else
    print_warning ".env file already exists. Skipping."
fi

# Create directories if needed
print_info "Creating necessary directories..."
mkdir -p logs
print_success "Directories created"

# Check if .env has been configured
print_info "Checking .env configuration..."
if grep -q "your_jira_api_token_here" .env 2>/dev/null; then
    print_warning ".env file needs configuration!"
    echo ""
    echo "To configure:"
    echo "  1. Get your Jira API token from: https://id.atlassian.com/manage-profile/security/api-tokens"
    echo "  2. Edit .env file and replace placeholders"
    echo ""
    read -p "Would you like to open .env now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} .env
    fi
fi

echo ""
print_success "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Make sure .env is configured with your Jira credentials"
echo "  2. Run: ${GREEN}./start.sh${NC} to start the application"
echo "  3. Open: ${BLUE}http://localhost:5000${NC} in your browser"
echo ""
echo "Or activate the virtual environment manually:"
echo "  ${GREEN}source venv/bin/activate${NC}"
echo "  ${GREEN}python app.py${NC}"
echo ""
