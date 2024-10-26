import uuid
from typing import List

from src.services.seed_service.types import OAuthInfo, Seed, SeedType
from src.stores.seed_store.seed_store import SeedStore


class SeedService:
    def __init__(self, seed_store: SeedStore):
        self.seed_store = seed_store

    def create_seed(
        self, user_id: uuid.UUID, auth_info: OAuthInfo, seed_type: SeedType
    ) -> Seed:
        seed_id = uuid.uuid4()
        with self.seed_store.session() as session:
            try:
                seed_orm = self.seed_store.create_seed(
                    session, seed_id, user_id, auth_info.model_dump(), seed_type
                )
                session.commit()
                return Seed.from_orm(seed_orm)
            except Exception as e:
                session.rollback()
                raise e

    def get_seed_by_user_id_and_seed_type(
        self, user_id: uuid.UUID, seed_type: SeedType
    ) -> Seed:
        with self.seed_store.session() as session:
            seed_orm = self.seed_store.get_seed_by_user_id_and_seed_type(
                session, user_id, seed_type
            )
            if seed_orm is None:
                return None
            return Seed.from_orm(seed_orm)

    def get_seeds_by_user_id(self, user_id: uuid.UUID) -> List[Seed]:
        with self.seed_store.session() as session:
            seed_orms = self.seed_store.get_seeds_by_user_id(session, user_id)
            return [Seed.from_orm(seed_orm) for seed_orm in seed_orms]

    def get_seed_by_id(self, user_id: uuid.UUID, seed_id: uuid.UUID) -> Seed:
        with self.seed_store.session() as session:
            seed_orm = self.seed_store.get_seed_by_id(session, user_id, seed_id)
            return Seed.from_orm(seed_orm)

    def update_seed_auth_info(self, seed_id: uuid.UUID, auth_info: OAuthInfo):
        with self.seed_store.session() as session:
            seed_orm = self.seed_store.update_seed_auth_info(
                session, seed_id, auth_info.model_dump()
            )
            session.commit()
            return Seed.from_orm(seed_orm)
