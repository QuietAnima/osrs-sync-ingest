# osrs-sync-ingest

Minimal ingestion service for OSRS sync data.

## Features
- FastAPI service with configurable `HOST` and `PORT`
- Endpoints:
  - `POST /osrs/sync/wikisync`
  - `POST /osrs/sync/containers`
- Bearer auth via `OSRS_SYNC_TOKEN`
- SQLite persistence (`OSRS_SYNC_DB_PATH`)
- Stores latest payload per source and appends event history with server timestamps
- No payload logging

## Environment
- `OSRS_SYNC_TOKEN` (required)
- `HOST` (default `127.0.0.1`)
- `PORT` (default `8089`)
- `OSRS_SYNC_DB_PATH` (default `./data/osrs_sync.db`)

## Run (local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env (set token)
uvicorn app:app --host 127.0.0.1 --port 8089
```

## Run (Docker Compose)
```bash
cp .env.example .env
# edit .env (set token)
# optional for Docker: set OSRS_SYNC_DB_PATH=/app/data/osrs_sync.db
docker compose up -d --build
```

See `deploy/install.md` for deployment options (systemd and Docker Compose).

## Security
Never commit secrets or endpoint values.
