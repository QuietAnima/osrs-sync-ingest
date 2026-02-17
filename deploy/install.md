# Install (Raspberry Pi)

```bash
mkdir -p /home/<user>/osrs-sync-ingest
cd /home/<user>/osrs-sync-ingest
# copy repository contents here
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and set OSRS_SYNC_TOKEN
```

Systemd (user or system):

```bash
sudo cp deploy/osrs-sync-ingest.service /etc/systemd/system/osrs-sync-ingest.service
sudo systemctl daemon-reload
sudo systemctl enable --now osrs-sync-ingest.service
sudo systemctl status osrs-sync-ingest.service
```

Docker Compose option:

```bash
cp .env.example .env
# edit .env and set OSRS_SYNC_TOKEN
# optional for Docker: set OSRS_SYNC_DB_PATH=/app/data/osrs_sync.db
docker compose up -d --build
docker compose logs -f
```
