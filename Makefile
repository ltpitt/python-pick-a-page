.PHONY: help test test-watch coverage clean install lint serve all

# Default target shows help
help:
	@echo "Available targets:"
	@echo "  make install      - Create venv and install dependencies"
	@echo "  make serve        - Start Flask server on port 8001"
	@echo "  make test         - Run all tests with coverage"
	@echo "  make test-watch   - Run tests in watch mode"
	@echo "  make coverage     - Generate detailed coverage report"
	@echo "  make lint         - Run code quality checks"
	@echo "  make clean        - Remove build artifacts and cache"
	@echo "  make all          - Run lint and test"

# Create virtual environment and install dependencies
install:
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment..."; \
		python -m venv .venv; \
	else \
		echo "Virtual environment already exists"; \
	fi
	@echo "Installing dependencies..."
	.venv/bin/pip install -r requirements.txt
	@echo "Installation complete! Activate with: source .venv/bin/activate"

# Start Flask server
serve:
	@echo "Starting Flask server on http://127.0.0.1:8001"
	source .venv/bin/activate && python -c "from backend.main import app; app.run(host='127.0.0.1', port=8001, debug=True)"

# Run tests with coverage
test:
	pytest -v --cov=backend --cov-report=term-missing

# Run tests in watch mode (requires pytest-watch)
test-watch:
	ptw -- -v --cov=backend

# Generate HTML coverage report
coverage:
	pytest --cov=backend --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Run linting (using built-in Python tools where possible)
lint:
	@echo "Running code quality checks..."
	python -m py_compile backend/**/*.py
	@echo "Syntax check passed!"

# Clean build artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf .pytest_cache htmlcov .coverage
	rm -rf *.egg-info dist build
	rm -rf output/
	@echo "Cleaned up build artifacts"

# Run all checks
all: lint test
	@echo "All checks passed!"
