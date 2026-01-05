"""Common Pydantic models for all agents."""

from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime


class WebhookPayload(BaseModel):
    """Generic incoming payload."""
    message: str | None = None
    data: dict[str, Any] | None = None


class AgentResponse(BaseModel):
    """Standard agent response format."""
    status: str = "ok"
    agent: str
    result: Any
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
