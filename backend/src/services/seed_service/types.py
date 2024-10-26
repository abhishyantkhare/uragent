import time
import uuid
from enum import Enum

from pydantic import BaseModel
from src.database.models.seed import SeedORM


class SeedType(str, Enum):
    TWITTER = "twitter"


class OAuthInfo(BaseModel):
    token_type: str = "bearer"
    access_token: str
    refresh_token: str
    expires_in: int
    scope: list[str]
    expires_at: float

    def is_token_expired(self):
        return self.expires_at < time.time()


class Seed(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    seed_type: SeedType
    auth_info: OAuthInfo

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, orm: SeedORM) -> "Seed":
        return cls(
            id=orm.id,
            user_id=orm.user_id,
            seed_type=orm.seed_type,
            auth_info=orm.auth_info,
        )

    def to_orm(self) -> SeedORM:
        return SeedORM(
            id=self.id,
            user_id=self.user_id,
            auth_info=self.auth_info,
            seed_type=self.seed_type,
        )
