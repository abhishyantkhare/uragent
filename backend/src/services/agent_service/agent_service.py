import uuid
from typing import List

from sqlalchemy.orm import Session
from src.services.agent_service.types import (
    Agent,
    AgentSeed,
    AgentSeedAction,
    AgentSeedFilter,
    AgentSeedFilterType,
    AgentSeedSource,
)
from src.services.seed_service.types import SeedType
from src.services.twitter_service.types import TwitterSeedSourceType
from src.stores.agent_store.agent_store import AgentStore
from src.stores.seed_store.seed_store import SeedStore


class AgentService:
    def __init__(self, agent_store: AgentStore, seed_store: SeedStore):
        self.agent_store = agent_store
        self.seed_store = seed_store

    def get_agents_for_user(self, user_id: uuid.UUID) -> List[Agent]:
        with self.agent_store.session() as session:
            agent_orms = self.agent_store.get_agents_for_user(session, user_id)
            if agent_orms is None:
                return []
            return [Agent.from_orm(agent_orm) for agent_orm in agent_orms]

    def create_agent(
        self, user_id: uuid.UUID, name: str, context: str, seed_ids: list[uuid.UUID]
    ) -> Agent:
        agent_id = uuid.uuid4()
        with self.agent_store.session() as session:
            try:
                agent_orm = self.agent_store.create_agent(
                    session, agent_id, user_id, name, context
                )
                for seed_id in seed_ids:
                    seed_actions = self._get_seed_actions(
                        session, user_id, seed_id, context
                    )
                    self.agent_store.create_agent_seed(
                        session, agent_id, seed_id, user_id, seed_actions.model_dump()
                    )
                session.commit()
                return Agent.from_orm(agent_orm)
            except Exception as e:
                session.rollback()
                raise e

    def get_agent_seeds(
        self, user_id: uuid.UUID, agent_id: uuid.UUID
    ) -> List[AgentSeed]:
        with self.agent_store.session() as session:
            agent_seeds = self.agent_store.get_agent_seeds(session, user_id, agent_id)
            return [AgentSeed.from_orm(agent_seed) for agent_seed in agent_seeds]

    def _get_seed_actions(
        self,
        session: Session,
        user_id: uuid.UUID,
        seed_id: list[uuid.UUID],
        context: str,
    ) -> AgentSeedAction:
        seed = self.seed_store.get_seed_by_id(session, seed_id, user_id)

        if seed.seed_type == SeedType.TWITTER:
            return AgentSeedAction(
                sources=[
                    AgentSeedSource(type=TwitterSeedSourceType.BOOKMARKS),
                    AgentSeedSource(type=TwitterSeedSourceType.FEED),
                ],
                filter=AgentSeedFilter(
                    type=AgentSeedFilterType.LLM,
                    query=context,
                ),
            )
