from acp_input import TerminalInputReader
from acp_interface import (
    TerminalInterface,
    InteractMode,
    InputCell,
    InputGrid,
    InputLayout,
)
from acp_output import TerminalPrinter, FilePrinter

layout = InputLayout()

interface = TerminalInterface(
    TerminalInputReader(), FilePrinter("outputs/test.txt"), InteractMode.MANUAL, layout
)

try:
    interface.loop()
except KeyboardInterrupt:
    interface.close()
