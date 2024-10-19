import uuid

from pydantic import BaseModel
from src.database.models.agent import AgentORM


class Agent(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, orm: AgentORM) -> "Agent":
        return cls(id=orm.id, user_id=orm.user_id, name=orm.name)

    def to_orm(self) -> AgentORM:
        return AgentORM(id=self.id, user_id=self.user_id, name=self.name)
