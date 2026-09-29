"""Minimale client voor Jira Cloud en Confluence Cloud (REST), herbruikbaar per klant.

Authenticatie: basic auth met e-mailadres + API-token
(https://id.atlassian.com/manage-profile/security/api-tokens).
"""

from __future__ import annotations

import os
import re
from typing import Iterator

import requests


class AtlassianError(RuntimeError):
    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


class AtlassianClient:
    def __init__(self, base_url: str, email: str, api_token: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.auth = (email, api_token)
        self.session.headers.update({"Accept": "application/json"})
        self.timeout = timeout

    @classmethod
    def from_env(cls, base_url: str, secrets_prefix: str = "") -> "AtlassianClient":
        """Leest ATLASSIAN_EMAIL/ATLASSIAN_TOKEN, of <PREFIX>_ATLASSIAN_EMAIL/_TOKEN als er een prefix is
        (voor een klant op een eigen Atlassian-site)."""
        prefix = f"{secrets_prefix}_" if secrets_prefix else ""
        email_var = f"{prefix}ATLASSIAN_EMAIL"
        token_var = f"{prefix}ATLASSIAN_TOKEN"
        email, token = os.environ.get(email_var), os.environ.get(token_var)
        if not email or not token:
            raise AtlassianError(f"{email_var} en/of {token_var} ontbreken in de omgeving (.env of GitHub secrets)")
        return cls(base_url, email, token)

    # ------------------------------------------------------------------ http

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
        if resp.status_code >= 400:
            raise AtlassianError(f"{method} {url} -> {resp.status_code}: {resp.text[:500]}", resp.status_code)
        return resp

    def _get(self, path: str, **params) -> dict:
        return self._request("GET", path, params=params).json()

    # ------------------------------------------------------------------ jira

    def search_issues(self, jql: str, fields: list[str]) -> Iterator[dict]:
        """Doorzoekt Jira met JQL (pagineert automatisch)."""
        token = None
        while True:
            body = {"jql": jql, "fields": fields, "maxResults": 100}
            if token:
                body["nextPageToken"] = token
            data = self._request("POST", "/rest/api/3/search/jql", json=body).json()
            yield from data.get("issues", [])
            token = data.get("nextPageToken")
            if not token or data.get("isLast", True):
                return

    def get_issue(self, key: str, fields: list[str]) -> dict:
        return self._get(f"/rest/api/3/issue/{key}", fields=",".join(fields))

    def get_issue_property(self, key: str, prop: str) -> dict | None:
        """Onzichtbare issue-eigenschap (entity property), of None als die niet bestaat."""
        try:
            return self._get(f"/rest/api/3/issue/{key}/properties/{prop}").get("value")
        except AtlassianError as e:
            if e.status == 404:
                return None
            raise

    def set_issue_property(self, key: str, prop: str, value: dict) -> None:
        self._request("PUT", f"/rest/api/3/issue/{key}/properties/{prop}", json=value)

    def add_comment(self, key: str, text: str, link: tuple[str, str] | None = None) -> None:
        """Plaatst een commentaar; `link` = (linktekst, url) wordt als klikbare link toegevoegd."""
        content: list[dict] = [{"type": "text", "text": text}]
        if link:
            content += [
                {"type": "text", "text": " "},
                {"type": "text", "text": link[0], "marks": [{"type": "link", "attrs": {"href": link[1]}}]},
            ]
        body = {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": content}]}
        self._request("POST", f"/rest/api/3/issue/{key}/comment", json={"body": body})

    def browse_url(self, key: str) -> str:
        return f"{self.base_url}/browse/{key}"

    # ------------------------------------------------------------ confluence

    def get_page(self, page_id: str, body_format: str | None = None) -> dict:
        params = {"body-format": body_format} if body_format else {}
        return self._get(f"/wiki/api/v2/pages/{page_id}", **params)

    def get_space_id(self, content_id: str) -> str:
        """Space-ID van een pagina of een Confluence-map (folder)."""
        try:
            return self.get_page(content_id)["spaceId"]
        except AtlassianError:
            return self._get(f"/wiki/api/v2/folders/{content_id}")["spaceId"]

    def create_page(self, space_id: str, parent_id: str, title: str, storage_xml: str) -> dict:
        body = {
            "spaceId": space_id,
            "status": "current",
            "title": title,
            "parentId": parent_id,
            "body": {"representation": "storage", "value": storage_xml},
        }
        return self._request("POST", "/wiki/api/v2/pages", json=body).json()

    def page_url(self, page: dict) -> str:
        webui = page.get("_links", {}).get("webui", "")
        return f"{self.base_url}/wiki{webui}" if webui else f"{self.base_url}/wiki/pages/viewpage.action?pageId={page['id']}"

    def find_page(self, space_id: str, title: str) -> dict | None:
        """Pagina met exact deze titel in de space, of None."""
        results = self._get("/wiki/api/v2/pages", **{"space-id": space_id, "title": title}).get("results", [])
        return results[0] if results else None

    def resolve_page_id(self, url: str) -> str | None:
        """Haalt het page-ID uit een Confluence-URL (ook korte /wiki/x/...-links)."""
        match = re.search(r"/pages/(?:edit-v2/)?(\d+)", url) or re.search(r"pageId=(\d+)", url)
        if match:
            return match.group(1)
        if "/wiki/x/" in url:
            resp = self._request("GET", url, allow_redirects=True)
            return self.resolve_page_id(resp.url) if resp.url != url else None
        return None
