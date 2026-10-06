from repopulse.database import Database


def test_database_snapshot(tmp_path):
    db = Database(str(tmp_path / "test.db"))
    db.initialise()
    db.insert_snapshot(
        {
            "owner": "python",
            "repo": "demo",
            "stars": 10,
            "forks": 2,
            "open_issues": 1,
            "watchers": 5,
            "size_kb": 100,
            "language": "Python",
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-01T00:00:00Z",
            "fetched_at": "2026-01-01T00:00:00Z",
        }
    )
    row = db.latest("python", "demo")
    assert row["stars"] == 10
