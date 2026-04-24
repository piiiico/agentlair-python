"""Stacks namespace — domain/DNS provisioning."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._http import HttpClient
    from ._types import ListStacksResult, Stack


class StacksNamespace:
    """Manage domain stacks."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    async def create(self, *, domain: str) -> Stack:
        """Create a new domain stack.

        Args:
            domain: Domain name to provision.
        """
        return await self._http.request("POST", "/v1/stack", body={"domain": domain})

    async def list(self) -> ListStacksResult:
        """List all domain stacks."""
        return await self._http.request("GET", "/v1/stack")
