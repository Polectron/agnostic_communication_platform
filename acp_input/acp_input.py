from abc import ABC, abstractmethod
from typing import Any, Optional


class AbstractInput(ABC):
    def __init__(self, value: Any) -> None:
        self.value = value


class StringInput(AbstractInput):
    def __init__(self, value: str) -> None:
        self.value = value


class AbstractInputReader(ABC):
    def __init__(self):
        self.input_queue = []

    def store_input(self, input: AbstractInput):
        self.input_queue.append(input)

    def get_input(self) -> Optional[AbstractInput]:
        if self.input_queue:
            return self.input_queue.pop(0)
        return None

    def read_input(self):
        self.store_input(self._read_input())

    @abstractmethod
    def _read_input(self) -> AbstractInput:
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()
