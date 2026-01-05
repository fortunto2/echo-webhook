from .base import BaseAgent
from .registry import AGENTS, register, get_agent, list_agents

# Import all agents to trigger registration
from . import echo
# from . import summarizer  # add new agents here

__all__ = ["BaseAgent", "AGENTS", "register", "get_agent", "list_agents"]
