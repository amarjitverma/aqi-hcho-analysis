# ============================================================
# AQI & HCHO Hotspot Analysis - Makefile
# ============================================================

.PHONY: help setup data preprocess train dashboard clean test lint format

help:
	@echo "Available commands:"
	@echo "  make setup      - Install dependencies and set up environment"
	@echo "  make data       - Download all data"
	@echo "  make preprocess - Run preprocessing pipeline"
	@echo "  make train      - Train model (usage: make train model=lstm)"
	@echo "  make dashboard  - Launch Streamlit dashboard"
	@echo "  make clean      - Remove cache and temporary files"
	@echo "  make test       - Run all tests"
	@echo "  make lint       - Run linting"
	@echo "  make format     - Format code with black"

setup:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install
	cp .env.example .env
	@echo "Setup complete. Edit .env with your API keys."

data:
	python scripts/download_data.py

preprocess:
	python scripts/preprocess.py

train:
	python scripts/train.py --model $(model)

dashboard:
	streamlit run dashboard/app.py

test:
	pytest tests/ -v --cov=src --cov-report=html

lint:
	flake8 src/
	mypy src/

format:
	black src/ scripts/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov/
	@echo "Clean complete."