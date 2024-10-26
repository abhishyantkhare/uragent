from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from src.dependencies.base_dependency import BaseDependency
from src.dependencies.database.database_session_dependency import (
    DatabaseSessionDependency,
)
from src.services.agent_service.agent_service import AgentService
from src.services.seed_service.seed_service import SeedService
from src.services.twitter_service.twitter_service import TwitterService
from src.services.user_service.user_service import UserService
from src.stores.agent_store.agent_store import AgentStore
from src.stores.seed_store.seed_store import SeedStore
from src.stores.user_store.user_store import UserStore

db_session_dependency = DatabaseSessionDependency(dependency_type=AsyncConnection)

user_store_dependency = BaseDependency(
    dependency_type=UserStore, sub_dependencies=[db_session_dependency]
)
user_service_dependency = BaseDependency(
    dependency_type=UserService, sub_dependencies=[user_store_dependency]
)
seed_store_dependency = BaseDependency(
    dependency_type=SeedStore, sub_dependencies=[db_session_dependency]
)
seed_service_dependency = BaseDependency(
    dependency_type=SeedService, sub_dependencies=[seed_store_dependency]
)
agent_store_dependency = BaseDependency(
    dependency_type=AgentStore, sub_dependencies=[db_session_dependency]
)
agent_service_dependency = BaseDependency(
    dependency_type=AgentService,
    sub_dependencies=[agent_store_dependency, seed_store_dependency],
)


twitter_service_dependency = BaseDependency(
    dependency_type=TwitterService, sub_dependencies=[seed_service_dependency]
)

# Clients
UserServiceClient = Annotated[UserService, Depends(user_service_dependency.get)]
AgentServiceClient = Annotated[AgentService, Depends(agent_service_dependency.get)]
TwitterServiceClient = Annotated[
    TwitterService, Depends(twitter_service_dependency.get)
]
SeedServiceClient = Annotated[SeedService, Depends(seed_service_dependency.get)]
