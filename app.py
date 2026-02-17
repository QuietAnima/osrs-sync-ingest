import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException, Request

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8089"))
DB_PATH = os.getenv("OSRS_SYNC_DB_PATH", "./data/osrs_sync.db")
TOKEN = os.getenv("OSRS_SYNC_TOKEN", "")

app = FastAPI(title="osrs-sync-ingest")


def _db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sync_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            payload TEXT NOT NULL,
            received_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sync_latest (
            source TEXT PRIMARY KEY,
            payload TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def _check_auth(auth_header: str | None):
    if not TOKEN:
        raise HTTPException(status_code=503, detail="Server token not configured")
    expected = f"Bearer {TOKEN}"
    if auth_header != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")


async def _ingest(source: str, request: Request, authorization: str | None):
    _check_auth(authorization)
    data = await request.json()
    payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    now = datetime.now(timezone.utc).isoformat()

    conn = _db()
    try:
        conn.execute(
            "INSERT INTO sync_events(source,payload,received_at) VALUES(?,?,?)",
            (source, payload, now),
        )
        conn.execute(
            """
            INSERT INTO sync_latest(source,payload,updated_at)
            VALUES(?,?,?)
            ON CONFLICT(source) DO UPDATE SET
              payload=excluded.payload,
              updated_at=excluded.updated_at
            """,
            (source, payload, now),
        )
        conn.commit()
    finally:
        conn.close()

    return {"ok": True, "source": source, "received_at": now}


@app.post("/osrs/sync/wikisync")
async def ingest_wikisync(request: Request, authorization: str | None = Header(default=None)):
    return await _ingest("wikisync", request, authorization)


@app.post("/osrs/sync/containers")
async def ingest_containers(request: Request, authorization: str | None = Header(default=None)):
    return await _ingest("containers", request, authorization)


@app.get("/health")
def health():
    return {"ok": True}
