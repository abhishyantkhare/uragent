import uuid

from sqlalchemy.orm import Session
from src.database.models.seed import SeedORM
from src.stores.base_store import BaseStore


class SeedStore(BaseStore):

    def create_seed(
        self,
        session: Session,
        seed_id: uuid.UUID,
        user_id: uuid.UUID,
        auth_info: dict,
        seed_type: str,
    ):
        seed = SeedORM(
            id=seed_id, user_id=user_id, auth_info=auth_info, seed_type=seed_type
        )
        session.add(seed)
        return seed

    def get_seed_by_user_id_and_seed_type(
        self, session: Session, user_id: uuid.UUID, seed_type: str
    ):
        return (
            session.query(SeedORM)
            .filter(SeedORM.user_id == user_id, SeedORM.seed_type == seed_type)
            .first()
        )

    def get_seeds_by_user_id(self, session: Session, user_id: uuid.UUID):
        return session.query(SeedORM).filter(SeedORM.user_id == user_id).all()

    def get_seed_by_id(self, session: Session, seed_id: uuid.UUID, user_id: uuid.UUID):
        return (
            session.query(SeedORM)
            .filter(SeedORM.id == seed_id, SeedORM.user_id == user_id)
            .first()
        )

    def update_seed_auth_info(self, session: Session, seed_id, auth_info: dict):
        session.query(SeedORM).filter(SeedORM.id == seed_id).update(
            {"auth_info": auth_info}
        )
