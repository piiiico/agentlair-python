"""Tests for client initialization and create_account."""

from __future__ import annotations

import httpx
import pytest
import respx

from agentlair import AgentLair, AgentLairClient, AgentLairSync


class TestClientInit:
    def test_default_base_url(self):
        client = AgentLair("al_test_key")
        assert client._http._base_url == "https://agentlair.dev"

    def test_custom_base_url(self):
        client = AgentLair("al_test_key", base_url="https://staging.agentlair.dev")
        assert client._http._base_url == "https://staging.agentlair.dev"

    def test_trailing_slash_stripped(self):
        client = AgentLair("al_test_key", base_url="https://agentlair.dev/")
        assert client._http._base_url == "https://agentlair.dev"

    def test_namespaces_exist(self):
        client = AgentLair("al_test_key")
        assert hasattr(client, "account")
        assert hasattr(client, "email")
        assert hasattr(client, "vault")
        assert hasattr(client, "trust")
        assert hasattr(client, "events")
        assert hasattr(client, "budget")
        assert hasattr(client, "calendar")
        assert hasattr(client, "observations")
        assert hasattr(client, "stacks")

    def test_legacy_alias(self):
        assert AgentLairClient is AgentLair


class TestCreateAccount:
    @pytest.mark.asyncio
    async def test_create_account(self, mock_api):
        mock_api.post("/v1/auth/keys").mock(
            return_value=httpx.Response(
                201,
                json={
                    "api_key": "al_live_new_key",
                    "key_prefix": "al_live_",
                    "account_id": "acc_123",
                    "tier": "free",
                    "created_at": "2026-04-23T00:00:00Z",
                    "warning": "Save your API key",
                    "limits": {},
                },
            )
        )
        result = await AgentLair.create_account(name="test-agent")
        assert result["api_key"] == "al_live_new_key"
        assert result["account_id"] == "acc_123"


class TestAsyncContextManager:
    @pytest.mark.asyncio
    async def test_context_manager(self):
        async with AgentLair("al_test_key") as client:
            assert client._http._base_url == "https://agentlair.dev"
        # After exit, client should be closed
