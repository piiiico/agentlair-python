"""Shared fixtures for AgentLair SDK tests."""

from __future__ import annotations

import pytest
import httpx
import respx

from agentlair import AgentLair


@pytest.fixture
def mock_api():
    """respx mock router scoped to the AgentLair base URL."""
    with respx.mock(base_url="https://agentlair.dev") as router:
        yield router


@pytest.fixture
def client():
    """An AgentLair client instance for testing."""
    return AgentLair("al_test_fake_key_for_testing")
