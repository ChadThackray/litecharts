.PHONY: lint test test-update-hashes

lint:
	uv run ruff format src/ tests/
	uv run ruff check src/ tests/ --fix
	uv run mypy src/ tests/ --strict

test:
	uv run pytest tests/ -v

test-update-hashes:
	uv run pytest tests/ -v --update-hashes
