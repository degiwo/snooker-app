ARG PYTHON_VERSION=3.14
FROM python:${PYTHON_VERSION}-slim AS build

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "snooker_backend.main:app", "--port", "8000", "--host", "0.0.0.0"]
