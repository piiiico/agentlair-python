"""Tests for events namespace."""

from __future__ import annotations

import json

import httpx
import pytest


class TestEvents:
    @pytest.mark.asyncio
    async def test_emit_single(self, client, mock_api):
        route = mock_api.post("/v1/events").mock(
            return_value=httpx.Response(
                200,
                json={
                    "accepted": 1,
                    "rejected": 0,
                    "errors": None,
                    "rate_limit": {"remaining": 99, "reset_at": "2026-04-23T13:00:00Z"},
                },
            )
        )
        result = await client.events.emit({
            "category": "tool",
            "action": "search",
            "result": "success",
        })
        assert result["accepted"] == 1
        # Verify auto-generated fields
        body = json.loads(route.calls[0].request.content)
        assert len(body) == 1
        assert "event_id" in body[0]
        assert "timestamp" in body[0]

    @pytest.mark.asyncio
    async def test_emit_batch(self, client, mock_api):
        route = mock_api.post("/v1/events").mock(
            return_value=httpx.Response(
                200,
                json={
                    "accepted": 2,
                    "rejected": 0,
                    "errors": None,
                    "rate_limit": {"remaining": 97, "reset_at": "2026-04-23T13:00:00Z"},
                },
            )
        )
        result = await client.events.emit([
            {"category": "tool", "action": "a", "result": "success"},
            {"category": "auth", "action": "b", "result": "failure"},
        ])
        assert result["accepted"] == 2
        body = json.loads(route.calls[0].request.content)
        assert len(body) == 2

    @pytest.mark.asyncio
    async def test_submit_alias(self, client, mock_api):
        mock_api.post("/v1/events").mock(
            return_value=httpx.Response(
                200,
                json={"accepted": 1, "rejected": 0, "errors": None, "rate_limit": {}},
            )
        )
        result = await client.events.submit({
            "category": "session",
            "action": "start",
            "result": "success",
        })
        assert result["accepted"] == 1
