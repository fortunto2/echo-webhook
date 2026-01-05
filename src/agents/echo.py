"""Echo agent - simple example that echoes back input."""

from typing import Any
from pydantic import BaseModel
from .base import BaseAgent
from .registry import register


# =============================================================================
# Models (each agent defines its own)
# =============================================================================

class EchoInput(BaseModel):
    """Input for echo agent - accepts anything."""
    message: str | None = None
    data: dict[str, Any] | None = None


class EchoOutput(BaseModel):
    """Output from echo agent."""
    agent: str = "echo"
    echo: Any


# =============================================================================
# Agent
# =============================================================================

@register
class EchoAgent(BaseAgent):
    """Simple agent that echoes back whatever is sent."""

    name = "echo"
    input_model = EchoInput
    output_model = EchoOutput

    async def run(self, input_data: Any) -> EchoOutput:
        """Echo input back."""
        return EchoOutput(echo=input_data)
