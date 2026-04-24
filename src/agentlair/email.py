"""Email namespace — claim addresses, send/receive email, webhooks."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ._http import HttpClient
    from ._types import (
        ClaimAddressResult,
        DeleteMessageResult,
        DeleteWebhookResult,
        FullMessage,
        GetInboxResult,
        ListAddressesResult,
        ListWebhooksResult,
        OutboxResult,
        SendEmailResult,
        UpdateMessageResult,
        Webhook,
    )


def _expand_address(address: str) -> str:
    """Expand bare name to full @agentlair.dev address."""
    if "@" not in address:
        return f"{address}@agentlair.dev"
    return address


class WebhooksNamespace:
    """Email webhook management."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    async def create(
        self,
        address: str,
        url: str,
        *,
        secret: str | None = None,
    ) -> Webhook:
        """Register a webhook for incoming emails."""
        body: dict[str, Any] = {
            "address": _expand_address(address),
            "url": url,
        }
        if secret is not None:
            body["secret"] = secret
        return await self._http.request("POST", "/v1/email/webhooks", body=body)

    async def list(self, *, address: str | None = None) -> ListWebhooksResult:
        """List registered webhooks."""
        query: dict[str, str] = {}
        if address:
            query["address"] = _expand_address(address)
        return await self._http.request("GET", "/v1/email/webhooks", query=query or None)

    async def delete(self, webhook_id: str) -> DeleteWebhookResult:
        """Delete a webhook by ID."""
        return await self._http.request("DELETE", f"/v1/email/webhooks/{webhook_id}")


class EmailNamespace:
    """Send and receive email through @agentlair.dev addresses."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self.webhooks = WebhooksNamespace(http)

    async def claim(
        self,
        address: str,
        *,
        public_key: str | None = None,
    ) -> ClaimAddressResult:
        """Claim an @agentlair.dev email address.

        Args:
            address: Bare name (``"my-agent"``) or full address
                     (``"my-agent@agentlair.dev"``).
            public_key: Base64url X25519 public key for E2E encryption.
        """
        body: dict[str, Any] = {"address": _expand_address(address)}
        if public_key is not None:
            body["public_key"] = public_key
        return await self._http.request("POST", "/v1/email/claim", body=body)

    async def addresses(self) -> ListAddressesResult:
        """List all claimed email addresses."""
        return await self._http.request("GET", "/v1/email/addresses")

    async def inbox(
        self,
        address: str,
        *,
        limit: int | None = None,
    ) -> GetInboxResult:
        """Get inbox messages for an address.

        Args:
            address: The email address to check.
            limit: Max messages to return (default 20, max 100).
        """
        query: dict[str, str] = {"address": _expand_address(address)}
        if limit is not None:
            query["limit"] = str(limit)
        return await self._http.request("GET", "/v1/email/inbox", query=query)

    async def read(self, message_id: str, address: str) -> FullMessage:
        """Read the full body of a message.

        Args:
            message_id: Use ``message_id_url`` from inbox results.
            address: The email address that received the message.
        """
        return await self._http.request(
            "GET",
            f"/v1/email/messages/{message_id}",
            query={"address": _expand_address(address)},
        )

    async def send(
        self,
        *,
        from_address: str,
        to: str | list[str],
        subject: str,
        text: str | None = None,
        html: str | None = None,
        in_reply_to: str | None = None,
    ) -> SendEmailResult:
        """Send an email.

        Args:
            from_address: Sender address (must be claimed).
            to: Recipient address(es).
            subject: Email subject line.
            text: Plain text body.
            html: HTML body.
            in_reply_to: Message-ID to reply to.
        """
        body: dict[str, Any] = {
            "from": _expand_address(from_address),
            "to": to if isinstance(to, list) else [to],
            "subject": subject,
        }
        if text is not None:
            body["text"] = text
        if html is not None:
            body["html"] = html
        if in_reply_to is not None:
            body["in_reply_to"] = in_reply_to
        return await self._http.request("POST", "/v1/email/send", body=body)

    async def outbox(self, *, limit: int | None = None) -> OutboxResult:
        """List sent messages."""
        query: dict[str, str] = {}
        if limit is not None:
            query["limit"] = str(limit)
        return await self._http.request("GET", "/v1/email/outbox", query=query or None)

    async def delete_message(
        self, message_id: str, address: str
    ) -> DeleteMessageResult:
        """Delete a message from the inbox."""
        return await self._http.request(
            "DELETE",
            f"/v1/email/messages/{message_id}",
            query={"address": _expand_address(address)},
        )

    async def update(
        self,
        message_id: str,
        address: str,
        *,
        read: bool | None = None,
    ) -> UpdateMessageResult:
        """Update a message (e.g. mark as read/unread)."""
        body: dict[str, Any] = {}
        if read is not None:
            body["read"] = read
        return await self._http.request(
            "PATCH",
            f"/v1/email/messages/{message_id}",
            query={"address": _expand_address(address)},
            body=body,
        )
