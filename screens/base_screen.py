from typing import Optional

import pygame
from pygame import Surface, SRCALPHA

from elements import Button
from game_settings import Settings


class BaseScreen:
    MENU_COVER_PATH = 'assets/snake-game-cover.jpg'

    def __init__(self, settings: Optional[Settings] = None, screen: Optional[Surface] = None):
        self.settings = settings if settings else Settings()
        self.screen = screen if screen else pygame.display.set_mode(self.settings.screen_dimensions)
        self.game_cover = pygame.transform.scale(surface=pygame.image.load(self.MENU_COVER_PATH),
                                                 size=self.settings.screen_dimensions)
        self.game_cover.fill((255, 255, 255, 180), None, pygame.BLEND_RGBA_MULT)
        self.mouse_position = pygame.mouse.get_pos()

    def _update_mouse_position(self):
        self.mouse_position = pygame.mouse.get_pos()

    def _get_button(self, text, y_position) -> Button:
        return Button(image=None,
                      pos=(self.settings.screen_width // 2, self.settings.screen_height // 6 * y_position),
                      text_input=text,
                      font=self.settings.get_font(size=75),
                      base_color="#d7fcd4",
                      hovering_color="White"
                      )

    def draw_default_background(self):
        self.screen.blit(self.game_cover, (0, 0))
        background_surface = pygame.Surface((self.settings.screen_width, self.settings.screen_height), SRCALPHA)
        background_surface.fill((0, 0, 0, 128))
        self.screen.blit(background_surface, (0, 0))
