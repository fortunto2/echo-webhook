"""
Cloudflare Python Worker - Agent Service

OpenAPI docs available at /docs
"""

from workers import WorkerEntrypoint
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from datetime import datetime
import asgi

from agents import AGENTS, get_agent, list_agents


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
# Universal Agent Endpoint
# =============================================================================

@app.post("/agents/{agent_name}")
async def run_agent(agent_name: str, request: Request):
    """Run any registered agent by name."""
    try:
        agent = get_agent(agent_name)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

    body = await request.json()

    # Validate input if agent has input_model
    try:
        validated_input = agent.validate_input(body)
    except ValidationError as e:
        return JSONResponse(status_code=422, content={"detail": e.errors()})

    # Run agent
    result = await agent.run(validated_input)

    # Return as dict if Pydantic model
    if hasattr(result, "model_dump"):
        return result.model_dump()
    return result


# =============================================================================
# Cloudflare Workers Entrypoint
# =============================================================================

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await asgi.fetch(app, request, self.env)
