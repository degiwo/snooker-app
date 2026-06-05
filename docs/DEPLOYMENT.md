# Hetzner Deployment Guide

This guide explains how to deploy the Snooker App to Hetzner using Docker Compose with secure credential management.

## Initial Server Setup

Edit your `.env` file with your desired PostgreSQL credentials:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password-here
POSTGRES_DB=snooker
```

**Important:** The `.env` file contains sensitive credentials and should **never** be committed to git. It's listed in `.gitignore`.

## Persistent Data

PostgreSQL data is stored in a Docker volume named `postgres_data`. This volume:
- Persists data across container restarts
- Survives `docker compose down` operations
- Is stored on the server's filesystem at `/var/lib/docker/volumes/snooker-app_postgres_data/_data/`

## Local Development

For local development, the process is similar but uses `docker-compose.yaml`:

```bash
# Create local .env file
cp .env.example .env

# Start services
docker compose up -d

# View logs
docker compose logs -f
```
