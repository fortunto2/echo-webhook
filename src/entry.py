"""
Cloudflare Python Worker - Agent Service

OpenAPI docs available at /docs
"""

from workers import WorkerEntrypoint
from fastapi import FastAPI, Request, HTTPException
from datetime import datetime
import uuid
import asgi

from core.models import AgentResponse
from agents import AGENTS, get_agent, list_agents


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
        "agents": list_agents(),
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


# =============================================================================
# Universal Agent Endpoint
# =============================================================================

@app.post("/agents/{agent_name}", response_model=AgentResponse)
async def run_agent(agent_name: str, request: Request):
    """Run any registered agent by name."""
    try:
        agent = get_agent(agent_name)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

    body = await request.json()
    return await agent.run(body)


# =============================================================================
# Cloudflare Workers Entrypoint
# =============================================================================

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await asgi.fetch(app, request, self.env)
