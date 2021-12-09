from functools import singledispatchmethod
import sys
import pygame

from acp_input.acp_input import AbstractInput, AbstractInputReader
from acp_interface import colors
from acp_interface.acp_interface import (
    AbstractInterface,
    BaseInputLayout,
    Button,
    ColumnLayout,
    GridLayout,
    InteractMode,
    RowLayout,
)
from acp_output.acp_output import AbstractOutputWriter

FPS = 32  # frames per second to update the screen
WINWIDTH = 1280
WINHEIGHT = 720


class VisualInterface(AbstractInterface):
    def __init__(
        self,
        input: AbstractInputReader,
        outputs: list[AbstractOutputWriter],
        mode: InteractMode,
        layout: BaseInputLayout,
    ):
        super().__init__(input, outputs, mode, layout)
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
        self.alpha_surface = self.surface.convert_alpha()
        pygame.display.set_caption("ACP VKeyboard")

        self.font = pygame.font.SysFont("Arial", 20, bold=True)

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
        raise NotImplementedError()

    @_render.register
    def _(self, input: GridLayout):
        for row in input.rows:
            self._render(row)

    @_render.register
    def _(self, input: RowLayout):
        for column in input.columns:
            self._render(column)

    @_render.register
    def _(self, input: ColumnLayout):
        offset = [0, 0]
        for item in input.items:
            self._render(item, offset)
            offset[0] += item.size[0]

    @_render.register
    def _(self, input: Button, offset: tuple[int, int]):

        origin = [*input.origin]

        for i in range(len(offset)):
            origin[i] += offset[i]

        tmp_surface = pygame.Surface(input.size)
        tmp_surface.fill(colors.WHITE)

        text = pygame.font.Font.render(self.font, input.label, True, colors.BLACK)
        text_size = text.get_size()
        tmp_surface.blit(
            text,
            (
                (input.size[0] / 2) - (text_size[0] / 2),
                (input.size[1] / 2) - (text_size[1] / 2),
            ),
        )

        pygame.draw.rect(
            tmp_surface,
            colors.BLACK,
            (0, 0, *input.size),
            width=5,
            border_radius=5,
        )

        self.surface.blit(tmp_surface, (*offset,))
