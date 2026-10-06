import csv
import json
import sqlite3
from pathlib import Path
from typing import Any


class Database:
    def __init__(self, path: str):
        self.path = path

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialise(self) -> None:
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner TEXT NOT NULL,
                    repo TEXT NOT NULL,
                    stars INTEGER NOT NULL,
                    forks INTEGER NOT NULL,
                    open_issues INTEGER NOT NULL,
                    watchers INTEGER NOT NULL,
                    size_kb INTEGER NOT NULL,
                    language TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    fetched_at TEXT NOT NULL
                )
            """)

    def insert_snapshot(self, snapshot: dict[str, Any]) -> None:
        columns = ", ".join(snapshot.keys())
        placeholders = ", ".join("?" for _ in snapshot)
        with self.connect() as conn:
            conn.execute(
                f"INSERT INTO snapshots ({columns}) VALUES ({placeholders})",
                tuple(snapshot.values()),
            )

    def latest(self, owner: str, repo: str) -> sqlite3.Row | None:
        with self.connect() as conn:
            return conn.execute(
                "SELECT * FROM snapshots WHERE owner = ? AND repo = ? ORDER BY id DESC LIMIT 1",
                (owner, repo),
            ).fetchone()

    def history(self, limit: int = 20) -> list[sqlite3.Row]:
        with self.connect() as conn:
            return conn.execute(
                "SELECT * FROM snapshots ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()

    def export(self, path: str, fmt: str) -> None:
        rows = self.history(10000)
        records = [dict(row) for row in rows]
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        if fmt == "json":
            Path(path).write_text(json.dumps(records, indent=2), encoding="utf-8")
        elif fmt == "csv":
            with open(path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=records[0].keys() if records else ["id"])
                writer.writeheader()
                writer.writerows(records)
        else:
            raise ValueError("format must be csv or json")
