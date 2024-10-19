from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar


T = TypeVar("T")


class BaseDependency(Generic[T]):

    def __init__(
        self, dependency_type: Type[T], sub_dependencies: list["BaseDependency"] = []
    ):
        self.dependency_type = dependency_type
        self.instance = None
        self.sub_dependencies = sub_dependencies

    async def get(self):
        if self.instance is None:
            await self._init_instance()
        yield self.instance

    async def _init_instance(self):
        sub_dependency_instances = []
        for sub_dependency in self.sub_dependencies:
            # hack to get the first item from the async generator
            async for sub_dependency_instance in sub_dependency.get():
                sub_dependency_instances.append(sub_dependency_instance)
                break
        self.instance = self.dependency_type(*sub_dependency_instances)
