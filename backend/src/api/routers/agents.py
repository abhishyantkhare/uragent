import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from src.api.auth import auth_required
from src.api.schemas.agents import CreateAgentRequest, ListAgentsResponse
from src.dependencies import AgentServiceClient
from src.services.agent_service.types import Agent
from src.services.user_service.types import User

router = APIRouter()


@router.get("/agents", response_model=ListAgentsResponse)
async def get_user_agents(
    user: Annotated[User, Depends(auth_required)], agent_service: AgentServiceClient
):
    agents = agent_service.get_agents_for_user(user.id)
    return ListAgentsResponse(agents=agents)


@router.post("/agents", response_model=Agent)
async def create_agent(
    request: CreateAgentRequest,
    user: Annotated[User, Depends(auth_required)],
    agent_service: AgentServiceClient,
):
    agent = agent_service.create_agent(
        user.id, request.name, request.context, request.seed_ids
    )
    return agent
