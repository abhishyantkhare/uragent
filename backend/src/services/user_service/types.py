import uuid

from pydantic import BaseModel
from src.database.models.user import UserORM


class User(BaseModel):
    id: uuid.UUID
    email: str
    clerk_id: str
    name: str | None = None

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, orm: UserORM) -> "User":
        return cls(id=orm.id, email=orm.email, clerk_id=orm.clerk_id, name=orm.name)

    def to_orm(self) -> UserORM:
        return UserORM(
            id=self.id, email=self.email, clerk_id=self.clerk_id, name=self.name
        )
