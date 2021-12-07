from abc import ABC, abstractmethod

from acp_input.acp_input import AbstractInput


class AbstractOutputWriter(ABC):
    @abstractmethod
    def write(self, input: AbstractInput):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()
