import uuid

from sqlalchemy import UUID, Column, String
from src.database.config import Base


class UserORM(Base):
    __tablename__ = "users"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: str = Column(String, unique=True, index=True)
    name: str = Column(String)
    clerk_id: str = Column(String)
