from acp_interface.acp_interface import AbstractInterface

import os

class TerminalInterface(AbstractInterface):
    def draw(self):
        os.system('clear')
