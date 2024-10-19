from src.dependencies.request_lifecycle_dependency import RequestLifecycleDependency
from src.database.config import engine
from sqlalchemy.orm import sessionmaker


class DatabaseSessionDependency(RequestLifecycleDependency):

    async def start(self):
        self.instance = sessionmaker(engine, expire_on_commit=False)

    async def stop(self):
        pass
