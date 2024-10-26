import uuid
from datetime import datetime

from sqlalchemy import JSON, UUID, Column, DateTime, ForeignKey, String
from src.database.config import Base


class AgentORM(Base):
    __tablename__ = "agents"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: str = Column(String)
    context: str = Column(String, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.now)
    updated_at: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("users.id"))


class AgentSeedORM(Base):
    __tablename__ = "agent_seeds"

    agent_id: uuid.UUID = Column(
        UUID(as_uuid=True), ForeignKey("agents.id"), primary_key=True
    )
    seed_id: uuid.UUID = Column(
        UUID(as_uuid=True), ForeignKey("seeds.id"), primary_key=True
    )
    user_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    actions: str = Column(JSON)
