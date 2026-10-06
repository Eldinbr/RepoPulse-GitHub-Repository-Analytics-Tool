from dataclasses import dataclass
from pathlib import Path
import os
import yaml


@dataclass(frozen=True)
class RepositoryConfig:
    name: str
    owner: str
    repo: str


@dataclass(frozen=True)
class AppConfig:
    database: str
    repositories: list[RepositoryConfig]


def load_config(path: str | Path) -> AppConfig:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    repositories = [RepositoryConfig(**item) for item in data.get("repositories", [])]
    if not repositories:
        raise ValueError("Configuration must contain at least one repository")
    return AppConfig(database=data.get("database", "repopulse.db"), repositories=repositories)


def github_token() -> str | None:
    return os.getenv("GITHUB_TOKEN")
