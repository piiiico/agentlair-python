"""Low-level async HTTP transport for AgentLair API."""

from __future__ import annotations

from typing import Any

import httpx

from .errors import _error_for_status

DEFAULT_BASE_URL = "https://agentlair.dev"
DEFAULT_TIMEOUT = 30.0


class HttpClient:
    """Thin wrapper around httpx.AsyncClient with auth and error handling."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            headers: dict[str, str] = {"Content-Type": "application/json"}
            if self._api_key:
                headers["Authorization"] = f"Bearer {self._api_key}"
            self._client = httpx.AsyncClient(
                base_url=self._base_url,
                headers=headers,
                timeout=self._timeout,
            )
        return self._client

    async def request(
        self,
        method: str,
        path: str,
        *,
        body: Any | None = None,
        query: dict[str, str] | None = None,
    ) -> Any:
        """Make an authenticated API request, returning parsed JSON."""
        client = self._get_client()
        response = await client.request(
            method,
            path,
            json=body,
            params=query,
        )
        # Parse response body
        data: Any = None
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type and response.content:
            data = response.json()
        elif response.content:
            data = response.text

        # Handle errors
        if response.status_code >= 400:
            message = "AgentLair API error"
            code = "unknown_error"
            if isinstance(data, dict):
                message = data.get("error", data.get("message", message))
                code = data.get("code", code)
            elif isinstance(data, str):
                message = data
            raise _error_for_status(response.status_code, message, code)

        return data

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
