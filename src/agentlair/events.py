"""Events namespace — behavioral event reporting for trust engine."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ._http import HttpClient
    from ._types import EmitEventResult, EventCategory, EventResultValue


class EventsNamespace:
    """Emit behavioral events consumed by the AgentLair trust engine."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    async def emit(
        self,
        events: dict[str, Any] | list[dict[str, Any]],
    ) -> EmitEventResult:
        """Emit one or more behavioral events.

        Each event dict should contain at minimum:
            - ``category``: One of tool, resource, auth, session,
              escalation, delegation, error.
            - ``action``: Free-form action name.
            - ``result``: One of success, failure, denied, timeout.

        Optional fields: ``resource_type``, ``duration_ms``,
        ``error_code``, ``scope_used``, ``metadata``, ``signature``,
        ``event_id``, ``timestamp``, ``session_id``.

        Missing ``event_id`` and ``timestamp`` are auto-generated.
        """
        if isinstance(events, dict):
            events = [events]

        # Auto-fill event_id and timestamp
        for event in events:
            if "event_id" not in event:
                event["event_id"] = str(uuid.uuid4())
            if "timestamp" not in event:
                event["timestamp"] = datetime.now(timezone.utc).isoformat()

        return await self._http.request(
            "POST", "/v1/events", body=events
        )

    async def submit(
        self,
        events: dict[str, Any] | list[dict[str, Any]],
    ) -> EmitEventResult:
        """Alias for :meth:`emit` — matches the task spec naming."""
        return await self.emit(events)
