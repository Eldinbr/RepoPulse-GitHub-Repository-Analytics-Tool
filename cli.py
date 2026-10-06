import argparse

from .api import GitHubClient
from .collector import collect
from .config import github_token, load_config
from .database import Database


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="repopulse", description="GitHub repository analytics CLI")
    parser.add_argument("--config", default="config.yaml")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("collect")
    sub.add_parser("summary")
    history = sub.add_parser("history")
    history.add_argument("--limit", type=int, default=20)
    export = sub.add_parser("export")
    export.add_argument("--format", choices=["csv", "json"], required=True)
    export.add_argument("--output", default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = load_config(args.config)
    db = Database(config.database)

    if args.command == "init":
        db.initialise()
        print(f"Database ready: {config.database}")
    elif args.command == "collect":
        results = collect(config, db, GitHubClient(token=github_token()))
        for result in results:
            item = result["config"]
            snapshot = result["snapshot"]
            print(f"[OK] {item.owner}/{item.repo} — {snapshot['stars']:,} stars — {snapshot['forks']:,} forks")
    elif args.command == "summary":
        db.initialise()
        rows = db.history(len(config.repositories))
        print("Repository       Stars    Forks    Issues    Language")
        print("-" * 54)
        for row in rows:
            print(f"{row['owner']}/{row['repo']:<14} {row['stars']:>6} {row['forks']:>8} {row['open_issues']:>9}    {row['language']}")
    elif args.command == "history":
        db.initialise()
        for row in db.history(args.limit):
            print(f"{row['fetched_at']} | {row['owner']}/{row['repo']} | stars={row['stars']} | forks={row['forks']}")
    elif args.command == "export":
        db.initialise()
        output = args.output or f"exports/repositories.{args.format}"
        db.export(output, args.format)
        print(f"Exported: {output}")
