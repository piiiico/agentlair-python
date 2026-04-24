"""Budget namespace — spending caps, charges, and approval flow."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ._http import HttpClient
    from ._types import (
        ApprovalActionResult,
        BudgetApproval,
        BudgetChargeResult,
        BudgetResult,
        ListApprovalsResult,
    )


class BudgetNamespace:
    """Manage spending caps and record charges with principal approval."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    async def set(
        self,
        *,
        daily: float | None = None,
        weekly: float | None = None,
        monthly: float | None = None,
        on_limit: str = "reject",
        single_tx_limit_cents: int | None = None,
    ) -> BudgetResult:
        """Set spending caps (amounts in atomic USDC, 1e-6 units).

        Args:
            daily: Daily spending cap.
            weekly: Weekly spending cap.
            monthly: Monthly spending cap.
            on_limit: ``"reject"`` or ``"approve"`` when limit is hit.
            single_tx_limit_cents: Max single transaction in cents.
        """
        body: dict[str, Any] = {"on_limit": on_limit}
        if daily is not None:
            body["daily"] = daily
        if weekly is not None:
            body["weekly"] = weekly
        if monthly is not None:
            body["monthly"] = monthly
        if single_tx_limit_cents is not None:
            body["single_tx_limit_cents"] = single_tx_limit_cents
        return await self._http.request("PUT", "/v1/budget", body=body)

    async def get(self) -> BudgetResult:
        """Get current budget caps and spending."""
        return await self._http.request("GET", "/v1/budget")

    async def charge(
        self,
        *,
        amount: float,
        category: str | None = None,
        description: str | None = None,
        reference_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> BudgetChargeResult:
        """Record a charge against the budget.

        Returns immediately on 200 (approved) or 202 (pending approval).
        Raises :class:`~agentlair.errors.PaymentRequiredError` on 402.
        """
        body: dict[str, Any] = {"amount": amount}
        if category is not None:
            body["category"] = category
        if description is not None:
            body["description"] = description
        if reference_id is not None:
            body["reference_id"] = reference_id
        if metadata is not None:
            body["metadata"] = metadata
        return await self._http.request("POST", "/v1/charge", body=body)

    async def approvals(
        self,
        status: str | None = None,
    ) -> ListApprovalsResult:
        """List approval requests.

        Args:
            status: Filter by status: pending, approved, rejected, expired.
        """
        query: dict[str, str] = {}
        if status is not None:
            query["status"] = status
        return await self._http.request("GET", "/v1/approvals", query=query or None)

    async def get_approval(self, approval_id: str) -> BudgetApproval:
        """Get a single approval by ID."""
        return await self._http.request("GET", f"/v1/approvals/{approval_id}")

    async def approve(self, approval_id: str) -> ApprovalActionResult:
        """Approve a pending charge."""
        return await self._http.request("POST", f"/v1/approvals/{approval_id}/approve")

    async def reject(
        self,
        approval_id: str,
        reason: str | None = None,
    ) -> ApprovalActionResult:
        """Reject a pending charge."""
        body: dict[str, Any] = {}
        if reason is not None:
            body["reason"] = reason
        return await self._http.request(
            "POST", f"/v1/approvals/{approval_id}/reject", body=body or None
        )
