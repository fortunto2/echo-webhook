"""Common Pydantic models - shared across agents."""

from pydantic import BaseModel
from typing import Any


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    detail: Any = None
