import uuid

from sqlalchemy.orm import Session
from src.database.models.agent import AgentORM
from src.stores.base_store import BaseStore


class AgentStore(BaseStore):
    def get_agents_for_user(self, session: Session, user_id: uuid.UUID):
        # ignore type checking for now
        return (
            session.query(AgentORM).filter(AgentORM.user_id == user_id).all()
        )  # noqa: E702

    def create_agent(
        self, session: Session, agent_id: uuid.UUID, user_id: uuid.UUID, name: str
    ):
        session.add(AgentORM(id=agent_id, user_id=user_id, name=name))
