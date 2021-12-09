from acp_input import TerminalInputReader
from acp_input.keyboard import KeyboardInputReader
from acp_interface import (
    TerminalInterface,
    InteractMode,
    BaseInputLayout,
)
from acp_interface.acp_interface import Button, GridLayout
from acp_interface.visual import VisualInterface
from acp_output import TerminalPrinter, FilePrinter
from acp_output.tts import TTSWriter

btn1 = Button((0, 0), (100, 50), label="BTN 1")
layout = GridLayout((0, 0), (50, 50))

interface = VisualInterface(
    KeyboardInputReader(), [TerminalPrinter(), TTSWriter()], InteractMode.MANUAL, btn1
)

try:
    interface.loop()
except KeyboardInterrupt:
    interface.close()
