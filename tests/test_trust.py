"""Tests for trust namespace."""

from __future__ import annotations

import httpx
import pytest


class TestTrust:
    @pytest.mark.asyncio
    async def test_score_own(self, client, mock_api):
        mock_api.get("/badge/me/score.json").mock(
            return_value=httpx.Response(
                200,
                json={
                    "agentId": "acc_abc",
                    "score": 72,
                    "confidence": 0.85,
                    "atfLevel": "senior",
                    "trend": "rising",
                    "dimensions": {
                        "consistency": {"score": 80, "confidence": 0.9},
                        "restraint": {"score": 70, "confidence": 0.8},
                        "transparency": {"score": 65, "confidence": 0.85},
                    },
                    "observationCount": 150,
                    "computedAt": "2026-04-23T12:00:00Z",
                },
            )
        )
        result = await client.trust.score()
        assert result["score"] == 72
        assert result["atfLevel"] == "senior"

    @pytest.mark.asyncio
    async def test_score_other(self, client, mock_api):
        mock_api.get("/badge/acc_xyz/score.json").mock(
            return_value=httpx.Response(
                200,
                json={
                    "agentId": "acc_xyz",
                    "score": 45,
                    "confidence": 0.5,
                    "atfLevel": "junior",
                    "trend": "stable",
                    "dimensions": {},
                    "observationCount": 10,
                    "computedAt": "2026-04-23T12:00:00Z",
                },
            )
        )
        result = await client.trust.score("acc_xyz")
        assert result["agentId"] == "acc_xyz"

    def test_badge_url_default(self, client):
        url = client.trust.badge("acc_123")
        assert url == "https://agentlair.dev/badge/acc_123"

    def test_badge_url_custom_style(self, client):
        url = client.trust.badge("acc_123", style="for-the-badge")
        assert url == "https://agentlair.dev/badge/acc_123?style=for-the-badge"
