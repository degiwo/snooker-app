# Snooker App

Track and analyze snooker drills and matches

## Run the application locally

```sh
docker compose -f compose.local.yml up --build
```

## Develop the application

```sh
cd backend
uv run uvicorn snooker_backend.main:app --reload
```

```sh
cd frontend
npm start
```
