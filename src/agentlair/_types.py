"""Shared type definitions for AgentLair Python SDK.

All types are TypedDicts for maximum compatibility and zero overhead.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict


# ---------------------------------------------------------------------------
# Account
# ---------------------------------------------------------------------------

class CreateAccountResult(TypedDict):
    api_key: str
    key_prefix: str
    account_id: str
    tier: str
    created_at: str
    warning: str
    limits: dict[str, Any]


class AccountMeResult(TypedDict):
    account_id: str
    tier: str
    created_at: str
    name: str | None
    recovery_email: str | None


class UsageResult(TypedDict):
    account_id: str
    tier: str
    period: str
    requests: dict[str, int]
    stacks: dict[str, int]
    emails: dict[str, Any]


class BillingResult(TypedDict):
    account_id: str
    tier: str


# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------

class ClaimAddressResult(TypedDict):
    address: str
    claimed: bool
    already_owned: bool
    account_id: str
    e2e_enabled: bool


class ListAddressesResult(TypedDict):
    addresses: list[str]
    count: int


class InboxMessage(TypedDict):
    message_id: str
    message_id_url: str
    from_: str  # mapped from "from"
    to: str
    subject: str
    snippet: str
    received_at: str
    read: bool


class GetInboxResult(TypedDict):
    messages: list[dict[str, Any]]
    has_more: bool
    count: int
    address: str


class FullMessage(TypedDict):
    message_id: str
    message_id_url: str
    subject: str
    received_at: str
    read: bool
    body: str | None
    html: str | None
    in_reply_to: str | None


class SendEmailResult(TypedDict):
    id: str
    status: str
    provider_id: str | None
    sent_at: str | None
    warning: str | None
    rate_limit: dict[str, int] | None


class OutboxMessage(TypedDict):
    id: str
    subject: str
    status: str
    queued_at: str
    sent_at: str | None
    error: str | None


class OutboxResult(TypedDict):
    messages: list[OutboxMessage]
    count: int


class DeleteMessageResult(TypedDict):
    deleted: bool
    message_id: str


class UpdateMessageResult(TypedDict):
    updated: bool
    message_id: str
    read: bool


# ---------------------------------------------------------------------------
# Email Webhooks
# ---------------------------------------------------------------------------

class Webhook(TypedDict):
    id: str
    address: str
    url: str
    created_at: str


class ListWebhooksResult(TypedDict):
    webhooks: list[Webhook]
    count: int


class DeleteWebhookResult(TypedDict):
    deleted: bool
    id: str


# ---------------------------------------------------------------------------
# Vault
# ---------------------------------------------------------------------------

class VaultPutResult(TypedDict):
    key: str
    stored: bool
    version: int
    created_at: str
    updated_at: str


class VaultGetResult(TypedDict):
    key: str
    ciphertext: str
    value: str
    metadata: dict[str, Any] | None
    version: int
    latest_version: int
    created_at: str
    updated_at: str


class VaultKeyInfo(TypedDict):
    key: str
    version: int
    metadata: dict[str, Any] | None
    created_at: str
    updated_at: str


class VaultListResult(TypedDict):
    keys: list[VaultKeyInfo]
    count: int
    limit: int
    tier: str


class VaultDeleteResult(TypedDict):
    key: str
    deleted: bool


# ---------------------------------------------------------------------------
# Stacks
# ---------------------------------------------------------------------------

class Stack(TypedDict):
    id: str
    domain: str
    status: str


class ListStacksResult(TypedDict):
    stacks: list[Stack]
    count: int


# ---------------------------------------------------------------------------
# Calendar
# ---------------------------------------------------------------------------

class CalendarEvent(TypedDict):
    id: str
    summary: str
    start: str
    end: str
    description: str | None
    location: str | None
    attendees: list[str] | None
    created_at: str


class CreateCalendarEventResult(TypedDict):
    event_id: str
    summary: str
    start: str
    end: str


class ListCalendarEventsResult(TypedDict):
    events: list[CalendarEvent]
    count: int
    total: int
    limit: int


class CalendarFeedResult(TypedDict):
    feed_url: str
    cal_token: str
    note: str
    how_to_subscribe: str


class DeleteCalendarEventResult(TypedDict):
    event_id: str
    deleted: bool


# ---------------------------------------------------------------------------
# Observations
# ---------------------------------------------------------------------------

class Observation(TypedDict):
    id: str
    topic: str
    content: str
    shared: bool
    agent_id: str
    display_name: str | None
    created_at: str


class ReadObservationsResult(TypedDict):
    observations: list[Observation]
    count: int
    filters: dict[str, Any]


class ObservationTopic(TypedDict):
    topic: str
    count: int
    latest: str


class ObservationsTopicsResult(TypedDict):
    topics: list[ObservationTopic]
    count: int


# ---------------------------------------------------------------------------
# Budget
# ---------------------------------------------------------------------------

class BudgetCap(TypedDict):
    limit_usdc: float
    spent_usdc: float


class BudgetResult(TypedDict):
    caps: dict[str, BudgetCap | None]
    on_limit: str


class BudgetChargeResult(TypedDict):
    charge_id: str | None
    approval_id: str | None
    reason: str | None
    expires_at: str | None
    exceeded: list[dict[str, Any]] | None


class BudgetApproval(TypedDict):
    id: str
    status: str
    amount_usdc: float
    category: str | None
    description: str | None
    reference_id: str | None
    reason: str | None
    created_at: str
    expires_at: str
    resolved_at: str | None


class ListApprovalsResult(TypedDict):
    approvals: list[BudgetApproval]
    count: int


class ApprovalActionResult(TypedDict):
    ok: bool
    id: str


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

EventCategory = Literal[
    "tool", "resource", "auth", "session",
    "escalation", "delegation", "error",
]

EventResultValue = Literal["success", "failure", "denied", "timeout"]


class EventError(TypedDict):
    event_id: str
    reason: str


class EmitEventResult(TypedDict):
    accepted: int
    rejected: int
    errors: list[EventError] | None
    rate_limit: dict[str, Any]


# ---------------------------------------------------------------------------
# Trust
# ---------------------------------------------------------------------------

class TrustDimension(TypedDict):
    score: float
    confidence: float


class TrustScoreResult(TypedDict):
    agentId: str
    score: float
    confidence: float
    atfLevel: str
    trend: str
    dimensions: dict[str, TrustDimension]
    observationCount: int
    computedAt: str


TrustBadgeStyle = Literal["flat", "flat-square", "for-the-badge"]
