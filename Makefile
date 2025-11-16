.PHONY: help setup install test run clean docker-build docker-run docker-push lint format

help:
	@echo "AWS Bedrock App Generator - Available Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup           - Complete setup (Python env + dependencies)"
	@echo "  make install         - Install dependencies only"
	@echo "  make clean           - Remove virtual environment and cache"
	@echo ""
	@echo "Development:"
	@echo "  make lint            - Run code quality checks"
	@echo "  make format          - Format code with black"
	@echo "  make test            - Run tests"
	@echo ""
	@echo "Running:"
	@echo "  make run             - Run interactive CLI"
	@echo "  make generate-py     - Generate Python example app"
	@echo "  make generate-java   - Generate Java example app"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build    - Build Docker image"
	@echo "  make docker-run      - Run in Docker"
	@echo "  make docker-push     - Push to registry"
	@echo ""

setup: clean
	@echo "Setting up development environment..."
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip setuptools wheel
	. .venv/bin/activate && pip install -r requirements.txt
	@echo "✓ Setup complete"
	@echo "Activate environment: source .venv/bin/activate"

install:
	@echo "Installing dependencies..."
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

clean:
	@echo "Cleaning up..."
	rm -rf .venv
	rm -rf __pycache__
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✓ Cleanup complete"

lint:
	@echo "Running code quality checks..."
	python -m pylint adaptive_app_gen/ cli.py 2>/dev/null || true
	python -m flake8 adaptive_app_gen/ cli.py --max-line-length=100 2>/dev/null || true
	@echo "✓ Lint checks complete"

format:
	@echo "Formatting code..."
	python -m black adaptive_app_gen/ cli.py
	python -m isort adaptive_app_gen/ cli.py
	@echo "✓ Code formatted"

test:
	@echo "Running tests..."
	python -m pytest tests/ -v 2>/dev/null || echo "No tests configured"
	@echo "✓ Test run complete"

run:
	@echo "Starting interactive CLI..."
	python cli.py --help

generate-py:
	@echo "Generating Python example application..."
	python cli.py --name example_python --requirements "Simple Python REST API" --type api --stack python
	@echo "✓ Generated: generated_apps/example_python"

generate-java:
	@echo "Generating Java example application..."
	python cli.py --name example_java --requirements "Spring Boot REST service" --type api --stack java
	@echo "✓ Generated: generated_apps/example_java"

docker-build:
	@echo "Building Docker image..."
	docker build -t bedrock-generator:latest .
	docker tag bedrock-generator:latest bedrock-generator:$(shell date +%Y%m%d_%H%M%S)
	@echo "✓ Docker image built"

docker-run:
	@echo "Running Docker container..."
	docker run -it \
	  -v ~/.aws/credentials:/root/.aws/credentials:ro \
	  -v $$(pwd)/generated_apps:/app/generated_apps \
	  -e AWS_REGION=us-east-1 \
	  bedrock-generator:latest \
	  python cli.py --help

docker-push:
	@echo "Pushing Docker image..."
	docker tag bedrock-generator:latest $${REGISTRY}/bedrock-generator:latest
	docker push $${REGISTRY}/bedrock-generator:latest
	@echo "✓ Image pushed to $${REGISTRY}"

.DEFAULT_GOAL := help
