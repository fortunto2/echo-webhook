"""Base agent class for all agents."""

from abc import ABC, abstractmethod
from typing import Any
from core.models import AgentResponse


class BaseAgent(ABC):
    """Base class for all agents."""

    name: str = "base"

    @abstractmethod
    async def run(self, input_data: Any) -> Any:
        """Process input and return result."""
        pass

    def response(self, result: Any) -> AgentResponse:
        """Wrap result in standard response format."""
        return AgentResponse(agent=self.name, result=result)
