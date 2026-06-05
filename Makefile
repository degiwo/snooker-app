.PHONY: backend-check

backend-check:
	cd apps/backend && uv run ruff check .
	cd apps/backend && uv run ruff format --check .
	cd apps/backend && uv run ty check .
