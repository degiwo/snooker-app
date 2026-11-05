# Snooker backend

Initialized with `uv init backend --app --package --name snooker_backend --python 3.14`.

## Commands

### Lint and format

```sh
uv run ruff check --fix
uv run ruff format
```

### Run backend

```sh
uv run uvicorn snooker_backend.main:app
```
