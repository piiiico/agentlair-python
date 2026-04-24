"""Calendar namespace — event scheduling and iCal feeds."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ._http import HttpClient
    from ._types import (
        CalendarFeedResult,
        CreateCalendarEventResult,
        DeleteCalendarEventResult,
        ListCalendarEventsResult,
    )


class CalendarNamespace:
    """Manage calendar events and iCal subscriptions."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    async def create_event(
        self,
        *,
        summary: str,
        start: str,
        end: str,
        description: str | None = None,
        location: str | None = None,
        attendees: list[str] | None = None,
    ) -> CreateCalendarEventResult:
        """Create a calendar event.

        Args:
            summary: Event title.
            start: Start time (ISO 8601).
            end: End time (ISO 8601).
            description: Optional description.
            location: Optional location.
            attendees: Optional list of attendee email addresses.
        """
        body: dict[str, Any] = {
            "summary": summary,
            "start": start,
            "end": end,
        }
        if description is not None:
            body["description"] = description
        if location is not None:
            body["location"] = location
        if attendees is not None:
            body["attendees"] = attendees
        return await self._http.request("POST", "/v1/calendar/events", body=body)

    async def list_events(
        self,
        *,
        from_date: str | None = None,
        to_date: str | None = None,
        limit: int | None = None,
    ) -> ListCalendarEventsResult:
        """List calendar events with optional date range.

        Args:
            from_date: Start of date range (ISO 8601 date).
            to_date: End of date range (ISO 8601 date).
            limit: Max events to return.
        """
        query: dict[str, str] = {}
        if from_date is not None:
            query["from"] = from_date
        if to_date is not None:
            query["to"] = to_date
        if limit is not None:
            query["limit"] = str(limit)
        return await self._http.request(
            "GET", "/v1/calendar/events", query=query or None
        )

    async def delete_event(self, event_id: str) -> DeleteCalendarEventResult:
        """Delete a calendar event."""
        return await self._http.request("DELETE", f"/v1/calendar/events/{event_id}")

    async def get_feed(self) -> CalendarFeedResult:
        """Get the iCal subscription feed URL."""
        return await self._http.request("GET", "/v1/calendar/feed")
