import uuid
from typing import List

from src.services.agent_service.types import Agent
from src.stores.agent_store.agent_store import AgentStore


class AgentService:
    def __init__(self, agent_store: AgentStore):
        self.agent_store = agent_store

    def get_agents_for_user(self, user_id: uuid.UUID) -> List[Agent]:
        with self.agent_store.session() as session:
            agent_orms = self.agent_store.get_agents_for_user(session, user_id)
            return [Agent.from_orm(agent_orm) for agent_orm in agent_orms]

    def create_agent(self, user_id: uuid.UUID, name: str) -> Agent:
        agent_id = uuid.uuid4()
        with self.agent_store.session() as session:
            try:
                agent_orm = self.agent_store.create_agent(
                    session, agent_id, user_id, name
                )
                session.commit()
                return Agent.from_orm(agent_orm)
            except Exception as e:
                session.rollback()
                raise e
