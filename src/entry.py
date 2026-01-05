"""
Cloudflare Python Worker - Agent Service

OpenAPI docs: /docs
"""

from workers import WorkerEntrypoint
from fastapi import FastAPI, Request
from datetime import datetime
import asgi

from agents import AGENTS, list_agents


# =============================================================================
# FastAPI App
# =============================================================================

app = FastAPI(title="Agent Service", docs_url="/docs")


# =============================================================================
# Health & Info
# =============================================================================

@app.get("/")
async def root():
    """List available agents with their input/output models."""
    agents_info = {}
    for name, cls in AGENTS.items():
        agents_info[name] = {
            "input": cls.input_model.model_json_schema() if cls.input_model else "any",
            "output": cls.output_model.model_json_schema() if cls.output_model else "any",
        }
    return {
        "service": "agent-service",
        "agents": agents_info,
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


# =============================================================================
# Agent Routes (auto-generated with proper schemas)
# =============================================================================

def create_agent_route(agent_cls):
    """Create a route handler for an agent with proper type hints."""
    input_model = agent_cls.input_model
    output_model = agent_cls.output_model

    if input_model and output_model:
        async def handler(payload: input_model) -> output_model:
            agent = agent_cls()
            return await agent.run(payload)
    elif input_model:
        async def handler(payload: input_model):
            agent = agent_cls()
            return await agent.run(payload)
    else:
        async def handler(request: Request):
            agent = agent_cls()
            body = await request.json()
            return await agent.run(body)

    handler.__doc__ = agent_cls.__doc__
    return handler


# Register routes for all agents
for name, agent_cls in AGENTS.items():
    handler = create_agent_route(agent_cls)
    app.post(
        f"/agents/{name}",
        response_model=agent_cls.output_model,
        name=f"agent_{name}",
        tags=["agents"]
    )(handler)


# =============================================================================
# Cloudflare Workers Entrypoint
# =============================================================================

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await asgi.fetch(app, request, self.env)
