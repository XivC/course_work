import abc
from abc import abstractmethod
from typing import Callable, Any


class ServiceBase(abc.ABC):

    def __call__(self) -> Any:
        for validator in self.get_validators():
            validator()

        return self.action()

    @abstractmethod
    def action(self):
        pass

    def get_validators(self) -> list[Callable]:
        return []
