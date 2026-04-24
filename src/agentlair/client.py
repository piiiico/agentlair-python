"""AgentLair client — main entry point for the Python SDK."""

from __future__ import annotations

import asyncio
from typing import Any

from ._http import DEFAULT_BASE_URL, HttpClient
from ._types import CreateAccountResult
from .account import AccountNamespace
from .budget import BudgetNamespace
from .calendar import CalendarNamespace
from .email import EmailNamespace
from .events import EventsNamespace
from .observations import ObservationsNamespace
from .stacks import StacksNamespace
from .trust import TrustNamespace
from .vault import VaultNamespace


class AgentLair:
    """Async-first client for the AgentLair API.

    Usage::

        import agentlair

        lair = agentlair.AgentLair("al_live_...")

        # Async usage
        score = await lair.trust.score()
        await lair.email.send(
            from_address="my-agent",
            to="someone@example.com",
            subject="Hello",
            text="Hi from my agent!",
        )

        # Don't forget to close when done
        await lair.close()

    Or use as an async context manager::

        async with agentlair.AgentLair("al_live_...") as lair:
            score = await lair.trust.score()
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ) -> None:
        self._http = HttpClient(api_key, base_url=base_url, timeout=timeout)

        # Namespaces
        self.account = AccountNamespace(self._http)
        self.email = EmailNamespace(self._http)
        self.vault = VaultNamespace(self._http)
        self.trust = TrustNamespace(self._http)
        self.events = EventsNamespace(self._http)
        self.budget = BudgetNamespace(self._http)
        self.calendar = CalendarNamespace(self._http)
        self.observations = ObservationsNamespace(self._http)
        self.stacks = StacksNamespace(self._http)

    @staticmethod
    async def create_account(
        *,
        name: str | None = None,
        email: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
    ) -> CreateAccountResult:
        """Create a new AgentLair account (no API key required).

        Args:
            name: Optional agent name.
            email: Optional recovery email.
            base_url: API base URL.

        Returns:
            Account details including the ``api_key``.
            **Save the API key immediately — it is not shown again.**
        """
        http = HttpClient(api_key=None, base_url=base_url)
        try:
            body: dict[str, Any] = {}
            if name is not None:
                body["name"] = name
            if email is not None:
                body["email"] = email
            return await http.request("POST", "/v1/auth/keys", body=body)
        finally:
            await http.close()

    async def close(self) -> None:
        """Close the underlying HTTP connection."""
        await self._http.close()

    async def __aenter__(self) -> AgentLair:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()


# Legacy alias for backward compatibility with the TS SDK naming
AgentLairClient = AgentLair


class AgentLairSync:
    """Synchronous wrapper around :class:`AgentLair`.

    Convenience class for scripts that don't need async::

        from agentlair import AgentLairSync

        lair = AgentLairSync("al_live_...")
        score = lair.trust_score()
        lair.close()

    Each method runs the async equivalent via ``asyncio.run()``.
    For production use, prefer the async :class:`AgentLair` client.
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ) -> None:
        self._client = AgentLair(api_key, base_url=base_url, timeout=timeout)

    def _run(self, coro: Any) -> Any:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # Already in an async context — use a new thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                return pool.submit(asyncio.run, coro).result()
        return asyncio.run(coro)

    # --- Account ---
    def account_me(self) -> Any:
        return self._run(self._client.account.me())

    def account_usage(self) -> Any:
        return self._run(self._client.account.usage())

    # --- Trust ---
    def trust_score(self, agent_id: str | None = None) -> Any:
        return self._run(self._client.trust.score(agent_id))

    def trust_badge(self, agent_id: str, style: str = "flat") -> str:
        return self._client.trust.badge(agent_id, style)  # type: ignore[arg-type]

    # --- Email ---
    def email_claim(self, address: str, **kwargs: Any) -> Any:
        return self._run(self._client.email.claim(address, **kwargs))

    def email_send(self, **kwargs: Any) -> Any:
        return self._run(self._client.email.send(**kwargs))

    def email_inbox(self, address: str, **kwargs: Any) -> Any:
        return self._run(self._client.email.inbox(address, **kwargs))

    # --- Vault ---
    def vault_store(self, key: str, value: str, **kwargs: Any) -> Any:
        return self._run(self._client.vault.store(key, value, **kwargs))

    def vault_get(self, key: str, **kwargs: Any) -> Any:
        return self._run(self._client.vault.get(key, **kwargs))

    def vault_list(self) -> Any:
        return self._run(self._client.vault.list())

    def vault_delete(self, key: str, **kwargs: Any) -> Any:
        return self._run(self._client.vault.delete(key, **kwargs))

    # --- Events ---
    def events_emit(self, events: Any) -> Any:
        return self._run(self._client.events.emit(events))

    # --- Budget ---
    def budget_get(self) -> Any:
        return self._run(self._client.budget.get())

    def budget_charge(self, **kwargs: Any) -> Any:
        return self._run(self._client.budget.charge(**kwargs))

    # --- Cleanup ---
    def close(self) -> None:
        self._run(self._client.close())

    @staticmethod
    def create_account(**kwargs: Any) -> Any:
        return asyncio.run(AgentLair.create_account(**kwargs))
