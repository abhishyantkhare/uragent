import uuid

from pydantic import BaseModel
from src.services.agent_service.types import AgentSeed
from src.services.seed_service.types import Seed


class AgentSeedingWorkflowInput(BaseModel):
    agent_id: uuid.UUID


class GetAgentSeedsParams(BaseModel):
    user_id: uuid.UUID
    agent_id: uuid.UUID


class ProcessTwitterSeedParams(BaseModel):
    agent_seed: AgentSeed
    twitter_seed: Seed
