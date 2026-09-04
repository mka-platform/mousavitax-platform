from __future__ import annotations
from typing import Any
from urllib.request import Request, urlopen
import json

class HttpPlatformServiceClient:
    """Minimal API adapter; authorization remains enforced by the destination API."""
    def __init__(self, base_url: str, token: str | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _get(self, path: str, actor_id: str) -> Any:
        headers = {"X-Agent-Actor": actor_id}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = Request(f"{self.base_url}{path}", headers=headers, method="GET")
        with urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))

    def get_case(self, case_id: str, actor_id: str): return self._get(f"/cases/{case_id}", actor_id)
    def list_cases(self, actor_id: str): return self._get("/cases", actor_id)
    def list_clients(self, actor_id: str): return self._get("/clients", actor_id)
    def list_deadlines(self, actor_id: str): return self._get("/deadlines", actor_id)
    def list_tasks(self, actor_id: str): return self._get("/tasks", actor_id)
