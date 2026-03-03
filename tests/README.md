# Tests

This directory contains automated tests for the Bug Reporter application.

## Test Files

- `test_app.py` - Python/Flask backend tests
- `test_frontend.js` - JavaScript frontend tests (Jest format)

## Running Tests

### All Tests

```bash
./run_tests.sh
```

This will run:
- ✅ Python unit tests with coverage
- ✅ JavaScript syntax validation
- ✅ CSS syntax validation

### Python Tests Only

```bash
# Activate virtual environment first
source venv/bin/activate

# Run tests
python -m pytest tests/test_app.py -v

# With coverage report
python -m pytest tests/test_app.py -v --cov=app --cov-report=html
```

### Individual Test

```bash
python -m pytest tests/test_app.py::TestBugReporter::test_health_endpoint -v
```

## Pre-Commit Hook

Tests automatically run before every commit. If tests fail, the commit is aborted.

To bypass (not recommended):
```bash
git commit --no-verify
```

## Test Coverage

Current test coverage:
- ✅ Health endpoint
- ✅ Index route
- ✅ Duplicate detection algorithm
- ✅ Similarity calculation
- ✅ Squad/Project selection logic
- ✅ Theme persistence
- ✅ File upload validation

## Adding New Tests

1. Add tests to `test_app.py` for backend features
2. Add tests to `test_frontend.js` for frontend features
3. Run `./run_tests.sh` to verify
4. Commit changes (tests will run automatically)

## Test Dependencies

Installed via `requirements-test.txt`:
- pytest
- pytest-cov
- pytest-mock
