import uuid

from pydantic import BaseModel
from src.services.agent_service.types import Agent


class ListAgentsResponse(BaseModel):
    agents: list[Agent]


class CreateAgentRequest(BaseModel):
    name: str
    context: str
    seed_ids: list[uuid.UUID]
