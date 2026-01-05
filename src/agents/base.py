"""Base agent class for all agents."""

from abc import ABC, abstractmethod
from typing import Any, Type
from pydantic import BaseModel


class BaseAgent(ABC):
    """Base class for all agents."""

    name: str = "base"
    input_model: Type[BaseModel] | None = None   # Override in subclass
    output_model: Type[BaseModel] | None = None  # Override in subclass

    def validate_input(self, data: dict) -> BaseModel | dict:
        """Validate input against model if defined."""
        if self.input_model:
            return self.input_model.model_validate(data)
        return data

    @abstractmethod
    async def run(self, input_data: Any) -> BaseModel | dict:
        """Process input and return result."""
        pass
