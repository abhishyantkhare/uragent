import uuid

from sqlalchemy.orm import Session
from src.database.models.user import UserORM
from src.stores.base_store import BaseStore


class UserStore(BaseStore):

    def create_user(
        self, session: Session, user_id: uuid.UUID, email: str, clerk_id: str
    ):
        session.add(UserORM(id=user_id, email=email, clerk_id=clerk_id))

    def get_user_by_email(self, session: Session, email: str):
        return session.query(UserORM).filter(UserORM.email == email).first()

    def get_user_by_clerk_id(self, session: Session, clerk_id: str):
        return session.query(UserORM).filter(UserORM.clerk_id == clerk_id).first()
