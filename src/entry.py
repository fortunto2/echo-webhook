"""
Cloudflare Python Worker - Agent Service

OpenAPI docs available at /docs
"""

from workers import WorkerEntrypoint
from fastapi import FastAPI, Request
from datetime import datetime
import uuid
import asgi

from core.models import AgentResponse
from agents import EchoAgent


# =============================================================================
# FastAPI App
# =============================================================================

app = FastAPI(title="Agent Service", docs_url="/docs")


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())[:8]
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# =============================================================================
# Health & Info
# =============================================================================

@app.get("/")
async def root():
    return {
        "service": "agent-service",
        "agents": ["echo"],
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


# =============================================================================
# Agents
# =============================================================================

@app.post("/agents/echo", response_model=AgentResponse)
async def agent_echo(request: Request):
    """Echo agent - returns whatever is sent."""
    body = await request.json()
    agent = EchoAgent()
    return await agent.run(body)


# =============================================================================
# Cloudflare Workers Entrypoint
# =============================================================================

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await asgi.fetch(app, request, self.env)
