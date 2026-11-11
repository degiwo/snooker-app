# Snooker App

Track and analyze snooker drills and matches

## Run the application locally

```sh
docker compose -f compose.local.yml up --build
```

## Develop the application

```sh
cd backend
uv sync
uv run uvicorn snooker_backend.main:app --reload
```

```sh
cd frontend
nvm use
npm install
npm start
```

## Git hooks

```sh
# The eslint and prettier hooks use versions from frontend,
# so run `npm install` in `frontend/` first.
prek run --all-files
```

## CI/CD

`.github/workflows/ci.yml`: A push to `main` (or a manual run)
deploys on the server, but only if all checks pass.
