from pydantic import BaseModel
from src.services.agent_service.types import Agent


class ListAgentsResponse(BaseModel):
    agents: list[Agent]
