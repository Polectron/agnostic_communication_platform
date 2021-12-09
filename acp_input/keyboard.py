import pygame
from pygame.constants import K_ESCAPE, K_RETURN, QUIT, KEYDOWN, KEYUP
from pygame.event import Event
from acp_input.acp_input import AbstractInputReader, CharKeyPressInput, PromptInput, QuitInput, SendInput, StringInput


class KeyboardInputReader(AbstractInputReader):

    def read_input(self):
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        for event in pygame.event.get():
            self._handle_event(event, alt_held, ctrl_held)

    def close(self):
        pass

    def _handle_event(self, event: Event, alt_held: bool, ctrl_held: bool):
        if event.type == QUIT:
            self.store_input(QuitInput(event))
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                self.store_input(PromptInput())
            if event.key == K_RETURN:
                self.store_input(SendInput())
            else:
                if event.unicode:
                    self.store_input(CharKeyPressInput(event, event.unicode))
        elif event.type == KEYDOWN:
            ...
