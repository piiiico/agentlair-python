"""Tests for account namespace."""

from __future__ import annotations

import httpx
import pytest


class TestAccount:
    @pytest.mark.asyncio
    async def test_me(self, client, mock_api):
        mock_api.get("/v1/account/me").mock(
            return_value=httpx.Response(
                200,
                json={
                    "account_id": "acc_abc",
                    "tier": "free",
                    "created_at": "2026-01-01T00:00:00Z",
                    "name": "test-agent",
                    "recovery_email": None,
                },
            )
        )
        result = await client.account.me()
        assert result["account_id"] == "acc_abc"
        assert result["tier"] == "free"
        assert result["name"] == "test-agent"

    @pytest.mark.asyncio
    async def test_usage(self, client, mock_api):
        mock_api.get("/v1/usage").mock(
            return_value=httpx.Response(
                200,
                json={
                    "account_id": "acc_abc",
                    "tier": "free",
                    "period": "2026-04",
                    "requests": {"used": 50, "limit": 100},
                    "stacks": {"used": 1, "limit": 3},
                    "emails": {"daily_used": 2, "daily_limit": 10},
                },
            )
        )
        result = await client.account.usage()
        assert result["requests"]["used"] == 50
