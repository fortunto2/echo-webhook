"""
Simple Echo Webhook - FastAPI on Cloudflare Workers
"""

from workers import WorkerEntrypoint
from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
from typing import Any
import asgi


# =============================================================================
# FastAPI App
# =============================================================================

app = FastAPI(title="Echo Webhook")


class WebhookPayload(BaseModel):
    """Incoming webhook payload"""
    message: str | None = None
    data: dict[str, Any] | None = None


@app.get("/")
async def root():
    return {"service": "echo-webhook", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.post("/webhook")
async def webhook(request: Request):
    """Echo back whatever is sent"""
    body = await request.json()
    
    return {
        "status": "ok",
        "received_at": datetime.utcnow().isoformat(),
        "echo": body
    }


@app.post("/webhook/typed")
async def webhook_typed(payload: WebhookPayload):
    """Echo with Pydantic validation"""
    
    return {
        "status": "ok",
        "received_at": datetime.utcnow().isoformat(),
        "echo": payload.model_dump()
    }


# =============================================================================
# Cloudflare Workers Entrypoint
# =============================================================================

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await asgi.fetch(app, request, self.env)
