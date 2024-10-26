import datetime
import uuid
from enum import Enum

from pydantic import BaseModel
from src.database.models.agent import AgentORM, AgentSeedORM


class Agent(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    context: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, orm: AgentORM) -> "Agent":
        return cls(
            id=orm.id,
            user_id=orm.user_id,
            name=orm.name,
            context=orm.context,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    def to_orm(self) -> AgentORM:
        return AgentORM(
            id=self.id,
            user_id=self.user_id,
            name=self.name,
            context=self.context,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class AgentSeedFilterType(str, Enum):
    LLM = "llm"


class AgentSeedSource(BaseModel):
    type: str


class AgentSeedFilter(BaseModel):
    type: AgentSeedFilterType
    query: str


class AgentSeedAction(BaseModel):
    sources: list[AgentSeedSource]
    filter: AgentSeedFilter


class AgentSeed(BaseModel):
    id: uuid.UUID
    agent_id: uuid.UUID
    seed_id: uuid.UUID
    user_id: uuid.UUID
    actions: AgentSeedAction

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, orm: AgentSeedORM) -> "AgentSeed":
        return cls.model_validate(orm)

    def to_orm(self) -> AgentSeedORM:
        return AgentSeedORM(
            id=self.id,
            agent_id=self.agent_id,
            seed_id=self.seed_id,
            user_id=self.user_id,
            actions=self.actions.model_dump(),
        )
