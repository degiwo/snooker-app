# Snooker backend

Initialized with `uv init backend --app --package --name snooker_backend --python 3.14`.

## Commands

### Lint and format

```sh
uv run ruff format
uv run ruff check --fix
```

### Run backend

```sh
uv run uvicorn snooker_backend.main:app
```
