#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }
print_info() { echo -e "${BLUE}ℹ${NC} $1"; }

echo ""
echo "🧪 Running Tests..."
echo "=================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d "venv" ]; then
        print_info "Activating virtual environment..."
        source venv/bin/activate
    else
        print_error "Virtual environment not found. Run ./setup.sh first"
        exit 1
    fi
fi

# Install test dependencies if needed
print_info "Checking test dependencies..."
pip install -q -r requirements-test.txt

# Run Python tests
print_info "Running Python tests..."
python -m pytest tests/test_app.py -v --cov=app --cov-report=term-missing

if [ $? -eq 0 ]; then
    print_success "Python tests passed!"
    echo ""
else
    print_error "Python tests failed!"
    exit 1
fi

# Check JavaScript syntax
print_info "Checking JavaScript syntax..."
node -c static/js/app.js

if [ $? -eq 0 ]; then
    print_success "JavaScript syntax check passed!"
    echo ""
else
    print_error "JavaScript syntax errors found!"
    exit 1
fi

# Check CSS syntax
print_info "Checking CSS syntax..."
# Simple CSS validation - check for common syntax errors
if grep -q "rgba([^)]*[^)']$" static/css/styles.css; then
    print_error "CSS syntax errors found (unclosed rgba)"
    exit 1
fi

print_success "CSS syntax check passed!"
echo ""

print_success "All tests passed! ✨"
echo ""
