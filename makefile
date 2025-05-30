default: test lint

init:
	pip install -e '.[test]'

test:
	true

lint:
	@echo "Running linter..."
	ruff check .

fix:
	@echo "Fixing issues with ruff..."
	ruff check . --fix

type:
	mypy kvasir
