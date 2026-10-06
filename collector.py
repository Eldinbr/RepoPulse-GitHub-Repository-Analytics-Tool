from datetime import datetime, timezone

from .api import GitHubClient
from .config import AppConfig
from .database import Database
from .metrics import extract_metrics


def collect(config: AppConfig, db: Database, client: GitHubClient) -> list[dict]:
    db.initialise()
    results = []
    for item in config.repositories:
        data = client.get_repository(item.owner, item.repo)
        metrics = extract_metrics(data)
        now = datetime.now(timezone.utc).isoformat()
        snapshot = {
            "owner": item.owner,
            "repo": item.repo,
            **metrics,
            "created_at": data.get("created_at", ""),
            "updated_at": data.get("updated_at", ""),
            "fetched_at": now,
        }
        previous = db.latest(item.owner, item.repo)
        db.insert_snapshot(snapshot)
        results.append({"config": item, "snapshot": snapshot, "previous": previous})
    return results
