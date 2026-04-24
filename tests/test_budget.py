"""Tests for budget namespace."""

from __future__ import annotations

import httpx
import pytest


class TestBudget:
    @pytest.mark.asyncio
    async def test_get_budget(self, client, mock_api):
        mock_api.get("/v1/budget").mock(
            return_value=httpx.Response(
                200,
                json={
                    "caps": {"daily": {"limit_usdc": 10.0, "spent_usdc": 2.5}},
                    "on_limit": "reject",
                },
            )
        )
        result = await client.budget.get()
        assert result["caps"]["daily"]["limit_usdc"] == 10.0

    @pytest.mark.asyncio
    async def test_set_budget(self, client, mock_api):
        mock_api.put("/v1/budget").mock(
            return_value=httpx.Response(
                200,
                json={
                    "caps": {"daily": {"limit_usdc": 20.0, "spent_usdc": 0}},
                    "on_limit": "approve",
                },
            )
        )
        result = await client.budget.set(daily=20.0, on_limit="approve")
        assert result["on_limit"] == "approve"

    @pytest.mark.asyncio
    async def test_charge_approved(self, client, mock_api):
        mock_api.post("/v1/charge").mock(
            return_value=httpx.Response(
                200,
                json={
                    "charge_id": "chg_123",
                    "approval_id": None,
                    "reason": None,
                    "expires_at": None,
                    "exceeded": None,
                },
            )
        )
        result = await client.budget.charge(
            amount=5.0, category="compute", description="GPU usage"
        )
        assert result["charge_id"] == "chg_123"
