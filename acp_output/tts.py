import pyttsx3

from acp_input.acp_input import AbstractInput
from acp_output.acp_output import AbstractOutputWriter


class TTSWriter(AbstractOutputWriter):
    def __init__(self):
        super().__init__()
        self.engine = pyttsx3.init()

    def write(self, input: str):
        self.engine.say(input)
        self.engine.runAndWait()

    def close(self):
        self.engine.stop()
