"""AgentLair error hierarchy."""

from __future__ import annotations


class AgentLairError(Exception):
    """Base error for all AgentLair API errors.

    Attributes:
        message: Human-readable error description.
        status: HTTP status code from the API response.
        code: Machine-readable error code (e.g. ``"address_taken"``).
    """

    def __init__(self, message: str, status: int, code: str) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code

    def __repr__(self) -> str:
        return f"AgentLairError(status={self.status}, code={self.code!r}, message={self.message!r})"


class AuthError(AgentLairError):
    """Raised on 401 Unauthorized responses."""


class NotFoundError(AgentLairError):
    """Raised on 404 Not Found responses."""


class RateLimitError(AgentLairError):
    """Raised on 429 Too Many Requests responses."""


class PaymentRequiredError(AgentLairError):
    """Raised on 402 Payment Required responses (budget exceeded)."""


class ConflictError(AgentLairError):
    """Raised on 409 Conflict responses (e.g. address already claimed)."""


def _error_for_status(status: int, message: str, code: str) -> AgentLairError:
    """Return the most specific error subclass for the given HTTP status."""
    cls = {
        401: AuthError,
        402: PaymentRequiredError,
        404: NotFoundError,
        409: ConflictError,
        429: RateLimitError,
    }.get(status, AgentLairError)
    return cls(message, status, code)
