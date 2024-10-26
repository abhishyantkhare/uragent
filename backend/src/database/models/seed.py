import uuid
from datetime import datetime

from sqlalchemy import JSON, UUID, Column, DateTime, ForeignKey, String
from src.database.config import Base


class SeedORM(Base):
    __tablename__ = "seeds"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seed_type: str = Column(String)
    auth_info: str = Column(JSON)
    created_at: datetime = Column(DateTime, default=datetime.now)
    updated_at: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("users.id"))
