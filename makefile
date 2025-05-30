default: test lint

init:
	pip install -e '.[test]'

test:
	true

lint:
	@echo "Running linters..."
	ruff check .
	black --check .

fix:
	@echo "Fixing issues with ruff..."
	ruff check . --fix

type:
	mypy kvasir
