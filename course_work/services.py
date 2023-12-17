import abc
from abc import abstractmethod
from typing import Callable


class ServiceBase(metaclass=abc.ABC):

    def __call__(self):
        for validator in self.get_validators():
            validator()

        self.action()

    @abstractmethod
    def action(self):
        pass

    def get_validators(self) -> list[Callable]:
        return []
