"""Tests for email namespace."""

from __future__ import annotations

import httpx
import pytest


class TestEmail:
    @pytest.mark.asyncio
    async def test_claim_bare_name(self, client, mock_api):
        route = mock_api.post("/v1/email/claim").mock(
            return_value=httpx.Response(
                200,
                json={
                    "address": "my-agent@agentlair.dev",
                    "claimed": True,
                    "already_owned": False,
                    "account_id": "acc_abc",
                    "e2e_enabled": False,
                },
            )
        )
        result = await client.email.claim("my-agent")
        assert result["claimed"] is True
        # Verify the bare name was expanded
        request = route.calls[0].request
        import json
        body = json.loads(request.content)
        assert body["address"] == "my-agent@agentlair.dev"

    @pytest.mark.asyncio
    async def test_claim_full_address(self, client, mock_api):
        route = mock_api.post("/v1/email/claim").mock(
            return_value=httpx.Response(
                200,
                json={
                    "address": "my-agent@agentlair.dev",
                    "claimed": True,
                    "already_owned": False,
                    "account_id": "acc_abc",
                    "e2e_enabled": False,
                },
            )
        )
        await client.email.claim("my-agent@agentlair.dev")
        import json
        body = json.loads(route.calls[0].request.content)
        assert body["address"] == "my-agent@agentlair.dev"

    @pytest.mark.asyncio
    async def test_send(self, client, mock_api):
        mock_api.post("/v1/email/send").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "status": "sent",
                    "provider_id": "prov_456",
                    "sent_at": "2026-04-23T12:00:00Z",
                    "warning": None,
                    "rate_limit": {"daily_remaining": 8, "hourly_remaining": 5},
                },
            )
        )
        result = await client.email.send(
            from_address="my-agent",
            to="someone@example.com",
            subject="Hello",
            text="Hi there!",
        )
        assert result["status"] == "sent"
        assert result["id"] == "msg_123"

    @pytest.mark.asyncio
    async def test_inbox(self, client, mock_api):
        mock_api.get("/v1/email/inbox").mock(
            return_value=httpx.Response(
                200,
                json={
                    "messages": [{"message_id": "m1", "subject": "Test"}],
                    "has_more": False,
                    "count": 1,
                    "address": "my-agent@agentlair.dev",
                },
            )
        )
        result = await client.email.inbox("my-agent", limit=10)
        assert result["count"] == 1
        assert result["messages"][0]["subject"] == "Test"

    @pytest.mark.asyncio
    async def test_addresses(self, client, mock_api):
        mock_api.get("/v1/email/addresses").mock(
            return_value=httpx.Response(
                200,
                json={"addresses": ["bot@agentlair.dev"], "count": 1},
            )
        )
        result = await client.email.addresses()
        assert result["count"] == 1
