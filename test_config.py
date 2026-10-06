from repopulse.config import load_config


def test_load_config(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text(
        "database: test.db\nrepositories:\n  - name: demo\n    owner: owner\n    repo: repo\n",
        encoding="utf-8",
    )
    config = load_config(path)
    assert config.database == "test.db"
    assert config.repositories[0].owner == "owner"
