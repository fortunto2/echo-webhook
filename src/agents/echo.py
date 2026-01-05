"""Echo agent - simple example that echoes back input."""

from typing import Any
from .base import BaseAgent
from .registry import register
from core.models import AgentResponse


@register
class EchoAgent(BaseAgent):
    """Simple agent that echoes back whatever is sent."""

    name = "echo"

    async def run(self, input_data: Any) -> AgentResponse:
        """Echo input back."""
        return self.response(result=input_data)
