from abc import ABC, abstractmethod

from acp_input.acp_input import AbstractInput


class AbstractOutputWriter(ABC):
    @abstractmethod
    def write(self, input: str):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()
