"""Tests for vault namespace."""

from __future__ import annotations

import httpx
import pytest


class TestVault:
    @pytest.mark.asyncio
    async def test_store(self, client, mock_api):
        mock_api.put("/v1/vault/my-secret").mock(
            return_value=httpx.Response(
                200,
                json={
                    "key": "my-secret",
                    "stored": True,
                    "version": 1,
                    "created_at": "2026-04-23T00:00:00Z",
                    "updated_at": "2026-04-23T00:00:00Z",
                },
            )
        )
        result = await client.vault.store("my-secret", "super-secret-value")
        assert result["stored"] is True
        assert result["version"] == 1

    @pytest.mark.asyncio
    async def test_get(self, client, mock_api):
        mock_api.get("/v1/vault/my-secret").mock(
            return_value=httpx.Response(
                200,
                json={
                    "key": "my-secret",
                    "ciphertext": "encrypted-blob",
                    "value": "encrypted-blob",
                    "metadata": None,
                    "version": 1,
                    "latest_version": 1,
                    "created_at": "2026-04-23T00:00:00Z",
                    "updated_at": "2026-04-23T00:00:00Z",
                },
            )
        )
        result = await client.vault.get("my-secret")
        assert result["key"] == "my-secret"
        assert result["version"] == 1

    @pytest.mark.asyncio
    async def test_list(self, client, mock_api):
        mock_api.get("/v1/vault/").mock(
            return_value=httpx.Response(
                200,
                json={
                    "keys": [{"key": "k1", "version": 2}],
                    "count": 1,
                    "limit": 100,
                    "tier": "free",
                },
            )
        )
        result = await client.vault.list()
        assert result["count"] == 1

    @pytest.mark.asyncio
    async def test_delete(self, client, mock_api):
        mock_api.delete("/v1/vault/old-key").mock(
            return_value=httpx.Response(
                200,
                json={"key": "old-key", "deleted": True, "versions_removed": 3},
            )
        )
        result = await client.vault.delete("old-key")
        assert result["deleted"] is True
