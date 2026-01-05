"""Agent registry - auto-registration for agents."""

from typing import Type
from .base import BaseAgent

# Registry of all agents: name -> class
AGENTS: dict[str, Type[BaseAgent]] = {}


def register(cls: Type[BaseAgent]) -> Type[BaseAgent]:
    """Decorator to register an agent class."""
    AGENTS[cls.name] = cls
    return cls


def get_agent(name: str) -> BaseAgent:
    """Get agent instance by name."""
    if name not in AGENTS:
        raise KeyError(f"Agent '{name}' not found. Available: {list(AGENTS.keys())}")
    return AGENTS[name]()


def list_agents() -> list[str]:
    """List all registered agent names."""
    return list(AGENTS.keys())
