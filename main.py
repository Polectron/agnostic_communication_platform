from acp_input import TerminalInputReader
from acp_interface import (
    TerminalInterface,
    InteractMode,
    InputCell,
    InputGrid,
    InputLayout,
)
from acp_output import TerminalPrinter

layout = InputLayout()

interface = TerminalInterface(
    TerminalInputReader(), TerminalPrinter(), InteractMode.MANUAL, layout
)

try:
    interface.loop()
except KeyboardInterrupt:
    interface.close()
