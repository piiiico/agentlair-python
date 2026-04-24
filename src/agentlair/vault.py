"""Vault namespace — zero-knowledge encrypted key-value store."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ._http import HttpClient
    from ._types import VaultDeleteResult, VaultGetResult, VaultListResult, VaultPutResult


class VaultNamespace:
    """Store and retrieve encrypted secrets in the AgentLair vault."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    async def put(
        self,
        key: str,
        *,
        ciphertext: str,
        metadata: dict[str, Any] | None = None,
    ) -> VaultPutResult:
        """Store an encrypted blob (versioned, append-only).

        Args:
            key: Vault key name.
            ciphertext: The encrypted value to store.
            metadata: Optional metadata dict.
        """
        body: dict[str, Any] = {"ciphertext": ciphertext}
        if metadata is not None:
            body["metadata"] = metadata
        return await self._http.request("PUT", f"/v1/vault/{key}", body=body)

    async def store(
        self,
        key: str,
        value: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> VaultPutResult:
        """Convenience method: store a plaintext value.

        Equivalent to ``put(key, ciphertext=value)`` — the server
        stores it opaquely regardless.
        """
        return await self.put(key, ciphertext=value, metadata=metadata)

    async def get(
        self,
        key: str,
        *,
        version: int | None = None,
    ) -> VaultGetResult:
        """Retrieve an encrypted blob.

        Args:
            key: Vault key name.
            version: Specific version number. Default: latest.
        """
        query: dict[str, str] = {}
        if version is not None:
            query["version"] = str(version)
        return await self._http.request(
            "GET", f"/v1/vault/{key}", query=query or None
        )

    async def list(self) -> VaultListResult:
        """List all vault keys (metadata only, no values)."""
        return await self._http.request("GET", "/v1/vault/")

    async def delete(
        self,
        key: str,
        *,
        version: int | None = None,
    ) -> VaultDeleteResult:
        """Delete a vault key (all versions or a specific version).

        Args:
            key: Vault key name.
            version: Specific version to delete. Default: all versions.
        """
        query: dict[str, str] = {}
        if version is not None:
            query["version"] = str(version)
        return await self._http.request(
            "DELETE", f"/v1/vault/{key}", query=query or None
        )
