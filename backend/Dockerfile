ARG PYTHON_VERSION=3.14
FROM python:${PYTHON_VERSION}-slim AS build

COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY . .
RUN uv sync --locked --no-dev --no-editable

FROM python:${PYTHON_VERSION}-slim
RUN useradd app

COPY --from=build /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

USER app
EXPOSE 8000

CMD ["uvicorn", "snooker_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
