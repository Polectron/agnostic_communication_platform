from acp_input.acp_input import AbstractInput, AbstractInputReader, StringInput


class TerminalInputReader(AbstractInputReader):
    def _read_input(self) -> AbstractInput:
        return StringInput(input())

    def close(self):
        pass
