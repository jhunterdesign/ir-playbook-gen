.PHONY: setup test lint format typecheck check clean

setup:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src tests
	ruff format --check src tests

format:
	ruff check --fix src tests
	ruff format src tests

typecheck:
	mypy src

# Everything CI runs, in one command
check: lint typecheck test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
