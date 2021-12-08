from acp_interface.acp_interface import AbstractInterface

import os
import platform

class TerminalInterface(AbstractInterface):
    def draw(self):
        if platform.system() in ("Linux", "Darwin"):
            os.system("clear")
        elif platform.system() == "Windows":
            os.system("cls")
        else:
            raise NotImplementedError()