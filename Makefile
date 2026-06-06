.PHONY: backend-check frontend-check

backend-check:
	cd apps/backend && uv run ruff check --select I --fix .
	cd apps/backend && uv run ruff format --check .
	cd apps/backend && uv run ty check .

frontend-check:
	cd apps/frontend && npm install --prefer-offline
	cd apps/frontend && npx prettier --check .
	cd apps/frontend && npm run build
	cd apps/frontend && npm run test
