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

btn1 = Button((0, 0), (150, 90), label="A", icon="images/apple.png", value="A")
btn2 = Button((0, 0), (150, 90), label="B", value="B")
btn3 = Button((0, 0), (150, 90), label="C", value="C")
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
