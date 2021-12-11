from functools import singledispatchmethod
import sys
import pygame
import math

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
    SelectableInput,
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

        self.font = pygame.font.SysFont("Arial", 40, bold=True)
        self._images_cache: dict[str, pygame.surface.Surface] = {}

    def draw(self):
        self.surface.fill(colors.WHITE)

        self._render(self.layout)
        self._draw_fps_counter()

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

        border = 5

        if input.icon:
            try:
                icon = self._load_image(input.icon)
                icon_size = icon.get_size()
                min_btn_size = min(*input.size)
                max_icon_size = max(*icon_size)
                ratio = 1
                if max_icon_size > min_btn_size:
                    ratio = max_icon_size / min_btn_size

                scaled_size = (
                    (icon_size[0] / ratio) - (border + 5),
                    (icon_size[1] / ratio) - (border + 5),
                )

                icon = pygame.transform.scale(icon, scaled_size)
                tmp_surface.blit(
                    icon,
                    (
                        (input.size[0] / 2) - (scaled_size[0] / 2),
                        (input.size[1] / 2) - (scaled_size[1] / 2),
                    ),
                )
            except Exception:
                pass

        if input.label:
            text = pygame.font.Font.render(self.font, input.label, True, colors.BLACK)
            text_size = text.get_size()
            tmp_surface.blit(
                text,
                (
                    (input.size[0] / 2) - (text_size[0] / 2),
                    (input.size[1] / 2) - (text_size[1] / 2),
                ),
            )

        border_color = colors.BLACK
        if self._is_selected(input):
            border_color = colors.RED

        pygame.draw.rect(
            tmp_surface,
            border_color,
            (0, 0, *input.size),
            width=border,
            border_radius=5,
        )

        self.surface.blit(tmp_surface, (*offset,))

    def _load_image(self, img_path: str):
        if img_path not in self._images_cache:
            self._images_cache[img_path] = pygame.image.load(img_path)
        return self._images_cache[img_path]

    def _is_selected(self, input: AbstractInput) -> bool:
        try:
            return input == self._selection_order_list[self._selected]
        except Exception:
            return False

    def _draw_fps_counter(self):
        fps_text = pygame.font.Font.render(
            self.font, str(math.ceil(self.fps_clock.get_fps())), True, colors.RED
        )
        fps_text_size = fps_text.get_size()
        self.surface.blit(
            fps_text,
            (self.surface.get_size()[0]-fps_text_size[0], self.surface.get_size()[1]-fps_text_size[1])
        )
