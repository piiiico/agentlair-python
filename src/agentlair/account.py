"""Account namespace — profile, usage, billing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ._http import HttpClient
    from ._types import AccountMeResult, BillingResult, UsageResult


class AccountNamespace:
    """Operations on the authenticated account."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    async def me(self) -> AccountMeResult:
        """Get current account profile."""
        return await self._http.request("GET", "/v1/account/me")

    async def usage(self) -> UsageResult:
        """Get usage statistics (requests, emails, stacks)."""
        return await self._http.request("GET", "/v1/usage")

    async def billing(self) -> BillingResult:
        """Get billing information."""
        return await self._http.request("GET", "/v1/billing")
