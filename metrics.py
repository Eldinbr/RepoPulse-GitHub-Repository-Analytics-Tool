from typing import Any


METRIC_FIELDS = ("stars", "forks", "open_issues", "watchers", "size_kb", "language")


def extract_metrics(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "stars": int(data.get("stargazers_count", 0)),
        "forks": int(data.get("forks_count", 0)),
        "open_issues": int(data.get("open_issues_count", 0)),
        "watchers": int(data.get("watchers_count", 0)),
        "size_kb": int(data.get("size", 0)),
        "language": data.get("language") or "Unknown",
    }


def calculate_change(current: int, previous: int | None) -> int:
    if previous is None:
        return current
    return current - previous


def percentage_change(current: int, previous: int | None) -> float | None:
    if previous in (None, 0):
        return None
    return round(((current - previous) / previous) * 100, 2)
