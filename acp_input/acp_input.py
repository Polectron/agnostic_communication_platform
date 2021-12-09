from abc import ABC, abstractmethod
from typing import Any, Optional

from pygame.event import Event


class AbstractInput(ABC):
    def __init__(self, value: Any) -> None:
        self.value = value


class StringInput(AbstractInput):
    def __init__(self, value: str) -> None:
        super().__init__(value)


class QuitInput(AbstractInput):
    def __init__(self, value: Any) -> None:
        super().__init__(value)


class KeyPressInput(AbstractInput):
    def __init__(self, value: Event) -> None:
        super().__init__(value)


class PromptInput(AbstractInput):
    def __init__(self) -> None:
        super().__init__(None)


class AbstractInputReader(ABC):
    def __init__(self):
        self.input_queue = []

    def store_input(self, input: AbstractInput):
        self.input_queue.append(input)

    def get_input(self) -> Optional[AbstractInput]:
        if self.input_queue:
            return self.input_queue.pop(0)
        return None

    @abstractmethod
    def read_input(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()
