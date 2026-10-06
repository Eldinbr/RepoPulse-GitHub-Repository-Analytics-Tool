import time
from typing import Any

import requests


class GitHubAPIError(RuntimeError):
    """Raised when the GitHub API cannot be queried successfully."""


class GitHubClient:
    def __init__(self, token: str | None = None, timeout: int = 15, retries: int = 3):
        self.timeout = timeout
        self.retries = retries
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/vnd.github+json", "User-Agent": "RepoPulse/1.0"})
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def get_repository(self, owner: str, repo: str) -> dict[str, Any]:
        url = f"https://api.github.com/repos/{owner}/{repo}"
        last_error: Exception | None = None
        for attempt in range(self.retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    return response.json()
                if response.status_code in {429, 500, 502, 503, 504}:
                    time.sleep(2**attempt)
                    continue
                raise GitHubAPIError(f"GitHub API returned {response.status_code}: {response.text}")
            except requests.RequestException as exc:
                last_error = exc
                if attempt < self.retries - 1:
                    time.sleep(2**attempt)
        raise GitHubAPIError(f"Unable to retrieve {owner}/{repo}: {last_error or 'request failed'}")
