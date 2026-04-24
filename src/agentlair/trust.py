"""Trust namespace — public trust scores and badge URLs."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._http import HttpClient
    from ._types import TrustBadgeStyle, TrustScoreResult


class TrustNamespace:
    """Query trust scores and generate badge URLs."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    async def score(self, agent_id: str | None = None) -> TrustScoreResult:
        """Get trust score for an agent.

        Args:
            agent_id: Account ID to look up. If ``None``, returns the
                      authenticated account's own score.
        """
        if agent_id:
            return await self._http.request(
                "GET", f"/badge/{agent_id}/score.json"
            )
        # For own score, use the authenticated endpoint
        return await self._http.request("GET", "/badge/me/score.json")

    def badge(
        self,
        agent_id: str,
        style: TrustBadgeStyle = "flat",
    ) -> str:
        """Return the badge image URL for an agent.

        This is a synchronous helper — no HTTP call is made.
        """
        base = self._http._base_url
        url = f"{base}/badge/{agent_id}"
        if style != "flat":
            url += f"?style={style}"
        return url
