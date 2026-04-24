"""Tests for error handling."""

from __future__ import annotations

import httpx
import pytest

from agentlair import AgentLairError, AuthError, ConflictError, RateLimitError
from agentlair.errors import NotFoundError, PaymentRequiredError


class TestErrors:
    @pytest.mark.asyncio
    async def test_401_raises_auth_error(self, client, mock_api):
        mock_api.get("/v1/account/me").mock(
            return_value=httpx.Response(
                401,
                json={"error": "Invalid API key", "code": "invalid_key"},
            )
        )
        with pytest.raises(AuthError) as exc_info:
            await client.account.me()
        assert exc_info.value.status == 401
        assert exc_info.value.code == "invalid_key"

    @pytest.mark.asyncio
    async def test_404_raises_not_found(self, client, mock_api):
        mock_api.get("/v1/vault/missing").mock(
            return_value=httpx.Response(
                404,
                json={"error": "Key not found", "code": "not_found"},
            )
        )
        with pytest.raises(NotFoundError):
            await client.vault.get("missing")

    @pytest.mark.asyncio
    async def test_409_raises_conflict(self, client, mock_api):
        mock_api.post("/v1/email/claim").mock(
            return_value=httpx.Response(
                409,
                json={"error": "Address already taken", "code": "address_taken"},
            )
        )
        with pytest.raises(ConflictError) as exc_info:
            await client.email.claim("taken")
        assert exc_info.value.code == "address_taken"

    @pytest.mark.asyncio
    async def test_429_raises_rate_limit(self, client, mock_api):
        mock_api.post("/v1/email/send").mock(
            return_value=httpx.Response(
                429,
                json={"error": "Too many requests", "code": "rate_limited"},
            )
        )
        with pytest.raises(RateLimitError):
            await client.email.send(
                from_address="bot", to="x@y.com", subject="Hi", text="Hello"
            )

    @pytest.mark.asyncio
    async def test_402_raises_payment_required(self, client, mock_api):
        mock_api.post("/v1/charge").mock(
            return_value=httpx.Response(
                402,
                json={"error": "Budget exceeded", "code": "budget_exceeded"},
            )
        )
        with pytest.raises(PaymentRequiredError):
            await client.budget.charge(amount=100.0)

    @pytest.mark.asyncio
    async def test_generic_error(self, client, mock_api):
        mock_api.get("/v1/account/me").mock(
            return_value=httpx.Response(
                500,
                json={"error": "Internal server error", "code": "internal"},
            )
        )
        with pytest.raises(AgentLairError) as exc_info:
            await client.account.me()
        assert exc_info.value.status == 500
        assert not isinstance(exc_info.value, AuthError)

    def test_error_repr(self):
        err = AgentLairError("something broke", 503, "service_unavailable")
        assert "503" in repr(err)
        assert "service_unavailable" in repr(err)

    def test_error_hierarchy(self):
        assert issubclass(AuthError, AgentLairError)
        assert issubclass(RateLimitError, AgentLairError)
        assert issubclass(NotFoundError, AgentLairError)
        assert issubclass(PaymentRequiredError, AgentLairError)
        assert issubclass(ConflictError, AgentLairError)
        assert issubclass(AgentLairError, Exception)
