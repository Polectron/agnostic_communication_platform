from functools import singledispatchmethod
import sys
import pygame

from acp_input.acp_input import AbstractInput, AbstractInputReader
from acp_interface import colors
from acp_interface.acp_interface import AbstractInterface, BaseInputLayout, InteractMode
from acp_output.acp_output import AbstractOutputWriter

FPS = 32  # frames per second to update the screen
WINWIDTH = 1280
WINHEIGHT = 720


class VisualInterface(AbstractInterface):
    def __init__(
        self,
        input: AbstractInputReader,
        output: AbstractOutputWriter,
        mode: InteractMode,
        layout: BaseInputLayout,
    ):
        super().__init__(input, output, mode, layout)
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
        self.alpha_surface = self.surface.convert_alpha()
        pygame.display.set_caption("ACP VKeyboard")

    def draw(self):
        self.surface.fill(colors.WHITE)

        self._render(self.layout)

        pygame.display.update()
        self.fps_clock.tick(FPS)

    def _quit(self):
        self.close()
        pygame.quit()
        sys.exit()

    @singledispatchmethod
    def _render(self, input: BaseInputLayout):
        pygame.draw.rect(self.surface, colors.BLACK, (*input.position, *input.size), width=5, border_radius=5)

    @_render.register
    def _render_layout(self, input: str):
        ...
