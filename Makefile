.PHONY: help test test-watch coverage clean install lint story all

# Default target shows help
help:
	@echo "Available targets:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run all tests with coverage"
	@echo "  make test-watch   - Run tests in watch mode"
	@echo "  make coverage     - Generate detailed coverage report"
	@echo "  make lint         - Run code quality checks"
	@echo "  make clean        - Remove build artifacts and cache"
	@echo "  make story        - Build example stories"
	@echo "  make all          - Run lint, test, and build stories"

# Install dependencies
install:
	pip install pytest pytest-cov pytest-watch

# Run tests with coverage
test:
	pytest -v --cov=pick_a_page --cov-report=term-missing

# Run tests in watch mode (requires pytest-watch)
test-watch:
	ptw -- -v --cov=pick_a_page

# Generate HTML coverage report
coverage:
	pytest --cov=pick_a_page --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Run linting (using built-in Python tools where possible)
lint:
	@echo "Running code quality checks..."
	python -m py_compile pick_a_page/*.py
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

# Build example stories (once implemented)
story:
	@echo "Building example stories..."
	@mkdir -p output
	@echo "Story building not yet implemented"

# Run all checks
all: lint test
	@echo "All checks passed!"
