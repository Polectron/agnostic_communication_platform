from typing import Optional
from acp_input.acp_input import (
    AbstractInput,
    AbstractInputReader,
    CharKeyPressInput,
    PromptInput,
    QuitInput,
    SendInput,
)
from acp_output.acp_output import AbstractOutputWriter

from enum import Enum
from collections import OrderedDict
from abc import ABC, abstractmethod
from functools import singledispatchmethod


class InteractMode(str, Enum):
    AUTOJUMP = "autojump"
    AUTOSELECT = "autoselect"
    MANUAL = "manual"


class LayoutPosition(str, Enum):
    CENTERED = "centered"
    TOPLEFT = "topleft"
    AUTO = "auto"


class BaseInputLayout(ABC):
    def __init__(
        self,
        origin: tuple[int, int],
        size: tuple[int, int],
        position: LayoutPosition = LayoutPosition.TOPLEFT,
    ):
        self.position = origin
        self.size = size
        self.center = position

        self.selected = False


class ColumnLayout(BaseInputLayout):
    def __init__(
        self,
        origin: tuple[int, int],
        size: tuple[int, int],
        position: LayoutPosition = LayoutPosition.TOPLEFT,
    ):
        super().__init__(origin, size, position=position)

        self.items: list[BaseInputLayout] = []
    
    def add(self, item: BaseInputLayout):
        self.items.append(item)

class RowLayout(BaseInputLayout):
    def __init__(
        self,
        origin: tuple[int, int],
        size: tuple[int, int],
        position: LayoutPosition = LayoutPosition.TOPLEFT,
        columns: int = 1,
    ):
        super().__init__(origin, size, position=position)
        self.columns: list[ColumnLayout] = [
            ColumnLayout((0, 0), (0, 0)) for _ in range(columns)
        ]

    def add(self, column: int, item: BaseInputLayout):
        self.columns[column].add(item)


class GridLayout(BaseInputLayout):
    def __init__(
        self,
        origin: tuple[int, int],
        size: tuple[int, int],
        position: LayoutPosition = LayoutPosition.TOPLEFT,
        rows: int = 1,
        columns: int = 1,
    ):
        super().__init__(origin, size, position=position)
        self.rows: list[RowLayout] = [
            RowLayout((0, 0), (0, 0), columns=columns) for _ in range(0, rows + 1)
        ]

    def add(self, row: int, column: int, item: BaseInputLayout):
        self.rows[row].add(column, item)


class Button(BaseInputLayout):
    def __init__(
        self,
        origin: tuple[int, int],
        size: tuple[int, int],
        position: LayoutPosition = LayoutPosition.TOPLEFT,
        label: Optional[str] = None,
        icon: Optional[str] = None,
    ):
        super().__init__(origin, size, position=position)
        self.label: Optional[str] = label
        self.icon: Optional[str] = icon


class AbstractInterface(ABC):
    def __init__(
        self,
        input: AbstractInputReader,
        outputs: list[AbstractOutputWriter],
        mode: InteractMode,
        layout: BaseInputLayout,
    ):
        self.input = input
        self.outputs = outputs
        self.mode = mode
        self.layout = layout
        # self.inputs_history: list[AbstractInput] = []

        self.input_buffer: list[CharKeyPressInput] = []

    @abstractmethod
    def draw(self):
        raise NotImplementedError()

    def loop(self):
        while True:
            self.draw()
            self.input.read_input()

            while i := self.input.get_input():
                self._handle_input(i)

    @abstractmethod
    def _quit():
        raise NotImplementedError()

    def close(self):
        self.input.close()
        for output in self.outputs:
            output.close()

    @singledispatchmethod
    def _handle_input(self, input: AbstractInput):
        raise NotImplementedError(f"Input type {type(input)} not handled")

    @_handle_input.register
    def _(self, input: QuitInput):
        self._quit()

    @_handle_input.register
    def _(self, input: CharKeyPressInput):
        self.input_buffer.append(input)

    @_handle_input.register
    def _(self, input: SendInput):
        tmp_string = ""
        for charkey in self.input_buffer:
            tmp_string += charkey.value
        for output in self.outputs:
            output.write(tmp_string)
        self.input_buffer.clear()

    @_handle_input.register
    def _(self, input: PromptInput):
        print("Opening options menu...")

    @abstractmethod
    def _render(self, input: BaseInputLayout):
        raise NotImplementedError(f"Input type {type(input)} not handled")
