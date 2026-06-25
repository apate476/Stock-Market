.PHONY: install test lint format

install:
	pip install -r requirements-dev.txt

test:
	pytest tests/ --cov=src --cov-report=term-missing

lint:
	ruff check src/ tests/

format:
	black src/ tests/
