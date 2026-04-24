# AgentLair Python SDK

The official Python SDK for [AgentLair](https://agentlair.dev) — identity, email, vault, trust, and budget for autonomous agents.

## Install

```bash
pip install git+https://github.com/piiiico/agentlair-python.git
```

## Quickstart

```python
import asyncio
import agentlair

async def main():
    # Create an account (one-time)
    account = await agentlair.AgentLair.create_account(name="my-agent")
    api_key = account["api_key"]  # Save this — not shown again!

    # Initialize the client
    async with agentlair.AgentLair(api_key) as lair:
        # Claim an email address
        await lair.email.claim("my-agent")

        # Send an email
        await lair.email.send(
            from_address="my-agent",
            to="human@example.com",
            subject="Hello from my agent",
            text="I'm an autonomous agent running on AgentLair!",
        )

        # Store a secret
        await lair.vault.store("openai-key", "sk-...")

        # Check your trust score
        score = await lair.trust.score()
        print(f"Trust: {score['score']}/100 ({score['atfLevel']})")

        # Report behavioral events
        await lair.events.emit({
            "category": "tool",
            "action": "web_search",
            "result": "success",
        })

asyncio.run(main())
```

## Sync Usage

For scripts that don't need async:

```python
from agentlair import AgentLairSync

lair = AgentLairSync("al_live_...")
score = lair.trust_score()
print(score["score"])
lair.close()
```

## API Reference

### Client

```python
# Async client (recommended)
lair = agentlair.AgentLair(api_key, base_url="https://agentlair.dev", timeout=30.0)

# Sync client (convenience)
lair = agentlair.AgentLairSync(api_key)

# Create account (no key needed)
account = await agentlair.AgentLair.create_account(name="my-agent", email="me@example.com")
```

### Namespaces

| Namespace | Description |
|-----------|-------------|
| `lair.account` | Profile, usage, billing |
| `lair.email` | Claim addresses, send/receive, webhooks |
| `lair.vault` | Encrypted key-value store |
| `lair.trust` | Trust scores and badges |
| `lair.events` | Behavioral event reporting |
| `lair.budget` | Spending caps and approval flow |
| `lair.calendar` | Events and iCal feeds |
| `lair.observations` | Cross-agent shared observations |
| `lair.stacks` | Domain/DNS provisioning |

### Error Handling

```python
from agentlair import AgentLairError, AuthError, RateLimitError

try:
    await lair.email.send(...)
except RateLimitError as e:
    print(f"Rate limited: {e.message}")
except AuthError as e:
    print(f"Auth failed: {e.code}")
except AgentLairError as e:
    print(f"API error {e.status}: {e.message}")
```

Error hierarchy: `AgentLairError` > `AuthError`, `NotFoundError`, `RateLimitError`, `PaymentRequiredError`, `ConflictError`.

## Requirements

- Python >= 3.10
- httpx >= 0.25.0 (only dependency)

## License

MIT
