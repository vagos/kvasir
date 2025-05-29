default: test lint

init:
	pip install -e '.[test]'

test:
	true

lint:
	@echo "Running linter..."
	ruff check .

type:
	python -m mypy kvasir
