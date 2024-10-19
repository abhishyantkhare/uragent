from abc import ABC, abstractmethod
import contextlib
from src.dependencies.base_dependency import BaseDependency


class RequestLifecycleDependency(ABC, BaseDependency):

    async def get(self):
        if self.instance is None:
            await self.start()
        try:
            yield self.instance
        finally:
            await self.stop()

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass
