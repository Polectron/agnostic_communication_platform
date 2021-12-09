from acp_input.acp_input import AbstractInput, AbstractInputReader, StringInput


class TerminalInputReader(AbstractInputReader):
    def read_input(self):
        self.store_input(StringInput(f"{input()}\n"))

    def close(self):
        pass
