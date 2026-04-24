"""Observations namespace — cross-agent shared observations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ._http import HttpClient
    from ._types import (
        Observation,
        ObservationsTopicsResult,
        ReadObservationsResult,
    )


class ObservationsNamespace:
    """Write and read cross-agent observations."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    async def write(
        self,
        *,
        topic: str,
        content: str,
        shared: bool = False,
        display_name: str | None = None,
    ) -> Observation:
        """Write an observation.

        Args:
            topic: Topic string for categorization.
            content: Observation content (max 10,000 chars).
            shared: Whether visible to other agents.
            display_name: Optional display name.
        """
        body: dict[str, Any] = {
            "topic": topic,
            "content": content,
            "shared": shared,
        }
        if display_name is not None:
            body["display_name"] = display_name
        return await self._http.request("POST", "/v1/observations", body=body)

    async def read(
        self,
        *,
        topic: str | None = None,
        agent_id: str | None = None,
        since: str | None = None,
        scope: str | None = None,
        limit: int | None = None,
    ) -> ReadObservationsResult:
        """Read observations with optional filters.

        Args:
            topic: Filter by topic.
            agent_id: Filter by agent.
            since: Only observations after this ISO 8601 timestamp.
            scope: ``"mine"``, ``"shared"``, or ``"all"``.
            limit: Max observations (default 50, max 200).
        """
        query: dict[str, str] = {}
        if topic is not None:
            query["topic"] = topic
        if agent_id is not None:
            query["agent_id"] = agent_id
        if since is not None:
            query["since"] = since
        if scope is not None:
            query["scope"] = scope
        if limit is not None:
            query["limit"] = str(limit)
        return await self._http.request(
            "GET", "/v1/observations", query=query or None
        )

    async def topics(self) -> ObservationsTopicsResult:
        """List all observation topics."""
        return await self._http.request("GET", "/v1/observations/topics")
