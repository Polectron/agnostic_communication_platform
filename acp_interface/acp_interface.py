from acp_input.acp_input import AbstractInput, AbstractInputReader
from acp_output.acp_output import AbstractOutputWriter

from enum import Enum
from collections import OrderedDict
from abc import ABC, abstractmethod


class InteractMode(str, Enum):
    AUTOJUMP = "autojump"
    AUTOSELECT = "autoselect"
    MANUAL = "manual"


class InputLayout(ABC):
    ...


class InputCell(ABC):
    def __init__(self, name: str, value: "InputCell"):
        self.name = name
        self.value: InputCell = value

    @abstractmethod
    def get_value(self):
        raise NotImplementedError()


class InputGrid(InputCell):
    def __init__(self, name: str, value):
        self.name = name
        self.grid: OrderedDict[str, InputCell] = value


class AbstractInterface(ABC):
    def __init__(
        self,
        input: AbstractInputReader,
        output: AbstractOutputWriter,
        mode: InteractMode,
        layout: InputLayout,
    ):
        self.input = input
        self.output = output
        self.mode = mode
        self.layout = layout
        self.inputs_history: list[AbstractInput] = []

    @abstractmethod
    def draw(self):
        raise NotImplementedError()

    def loop(self):
        while True:
            self.draw()
            self.input.read_input()
            inputs: list[AbstractInput] = []
            while i := self.input.get_input():
                inputs.append(i)

            for input in inputs:
                if input == "!!!":
                    ...
                else:
                    self.output.write(input)

    def close(self):
        self.input.close()
        self.output.close()
