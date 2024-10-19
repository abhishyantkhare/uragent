import uuid

from src.api.schemas.users import SignInMethod
from src.services.user_service.types import User
from src.stores.user_store.user_store import UserStore


class UserService:
    def __init__(self, user_store: UserStore):
        self.user_store = user_store

    def create_user(
        self, email: str, name: str, clerk_id: str, sign_in_method: SignInMethod
    ) -> User:
        """
        Checks if the user already exists, if not creates a new user.
        """
        user_id = uuid.uuid4()
        with self.user_store.session() as session:
            try:
                if sign_in_method == SignInMethod.CLERK:
                    user_orm = self.user_store.get_user_by_clerk_id(session, clerk_id)
                else:
                    user_orm = self.user_store.get_user_by_email(session, email)
                if user_orm:
                    return User.from_orm(user_orm)
                new_user_orm = self.user_store.create_user(
                    session, user_id, email, clerk_id, name
                )
                session.commit()
                return User.from_orm(new_user_orm)
            except Exception as e:
                session.rollback()
                raise e

    def get_user_by_clerk_id(self, clerk_id: str) -> User | None:
        with self.user_store.session() as session:
            user_orm = self.user_store.get_user_by_clerk_id(session, clerk_id)
            return User.from_orm(user_orm) if user_orm else None
