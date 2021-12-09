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
btn2 = Button((0, 0), (100, 50), label="BTN 2")
btn3 = Button((0, 0), (100, 50), label="BTN 3")
layout = GridLayout((0, 0), (50, 50))
layout.add(0, 0, btn1)
layout.add(0, 0, btn2)
layout.add(0, 0, btn3)

interface = VisualInterface(
    KeyboardInputReader(), [TerminalPrinter(), TTSWriter()], InteractMode.MANUAL, layout
)

try:
    interface.loop()
except KeyboardInterrupt:
    interface.close()
