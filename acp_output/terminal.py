from acp_input.acp_input import AbstractInput
from acp_output.acp_output import AbstractOutputWriter


class TerminalPrinter(AbstractOutputWriter):
    def write(self, input: AbstractInput):
        print(input.value)

    def close(self):
        pass
