import uuid

from sqlalchemy.orm import Session
from src.database.models.agent import AgentORM, AgentSeedORM
from src.stores.base_store import BaseStore


class AgentStore(BaseStore):
    def get_agents_for_user(self, session: Session, user_id: uuid.UUID):
        # ignore type checking for now
        return (
            session.query(AgentORM).filter(AgentORM.user_id == user_id).all()
        )  # noqa: E702

    def create_agent(
        self,
        session: Session,
        agent_id: uuid.UUID,
        user_id: uuid.UUID,
        name: str,
        context: str,
    ):
        agent = AgentORM(id=agent_id, user_id=user_id, name=name, context=context)
        session.add(agent)
        return agent

    def create_agent_seed(
        self,
        session: Session,
        agent_id: uuid.UUID,
        seed_id: uuid.UUID,
        user_id: uuid.UUID,
        actions: dict,
    ):
        session.add(
            AgentSeedORM(
                agent_id=agent_id, seed_id=seed_id, user_id=user_id, actions=actions
            )
        )

    def get_agent_seeds(
        self, session: Session, user_id: uuid.UUID, agent_id: uuid.UUID
    ):
        return (
            session.query(AgentSeedORM)
            .filter(AgentSeedORM.agent_id == agent_id, AgentSeedORM.user_id == user_id)
            .all()
        )
