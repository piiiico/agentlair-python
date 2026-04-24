"""AgentLair Python SDK — identity, email, vault, trust, and budget for autonomous agents.

Usage::

    import agentlair

    # Async (recommended)
    async with agentlair.AgentLair("al_live_...") as lair:
        score = await lair.trust.score()
        await lair.email.send(from_address="my-agent", to="x@y.com", subject="Hi", text="Hello!")

    # Sync (convenience)
    lair = agentlair.AgentLairSync("al_live_...")
    score = lair.trust_score()
    lair.close()
"""

from .client import AgentLair, AgentLairClient, AgentLairSync
from .errors import (
    AgentLairError,
    AuthError,
    ConflictError,
    NotFoundError,
    PaymentRequiredError,
    RateLimitError,
)

__version__ = "0.1.0"

__all__ = [
    # Clients
    "AgentLair",
    "AgentLairClient",
    "AgentLairSync",
    # Errors
    "AgentLairError",
    "AuthError",
    "ConflictError",
    "NotFoundError",
    "PaymentRequiredError",
    "RateLimitError",
    # Version
    "__version__",
]
