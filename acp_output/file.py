from acp_input.acp_input import AbstractInput
from acp_output.acp_output import AbstractOutputWriter


class FilePrinter(AbstractOutputWriter):

    def __init__(self, filename: str):
        self.file = open(filename, "a")

    def write(self, input: str):
        self.file.write(input)

    def close(self):
        self.file.close()
