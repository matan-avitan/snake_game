import sys
from typing import Optional

import pygame
from pygame import SRCALPHA, Surface

from elements import Button
from game_settings import Settings
from screens.base_screen import BaseScreen
from screens.game.game import Game
from screens.leaderboard.leaderboard import Leaderboard
from screens.options.options import Options


class Menu(BaseScreen):
    MENU_COVER_PATH = 'assets/snake-game-cover.jpg'

    def __init__(self, settings: Optional[Settings] = None, screen: Optional[Surface] = None):
        pygame.init()
        super().__init__(settings=settings, screen=screen)
        pygame.display.set_caption('Snake Game')
        self.play_button = self._get_button(text="Play", y_position=2)
        self.options_button = self._get_button(text="Options", y_position=3)
        self.leaderboard_button = self._get_button(text="Leader Board", y_position=4)
        self.quit_button = self._get_button(text="Quit", y_position=5)

    def _get_font(self, size):
        return pygame.font.SysFont(self.settings.game_font, size=size)

    def _draw_title(self):
        menu_text = self.settings.get_font(size=150).render('Menu', True, "#ebedbe")
        menu_rect = menu_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 6))
        self.screen.blit(menu_text, menu_rect)

    def _draw_buttons(self):
        for button in [self.play_button, self.options_button, self.leaderboard_button, self.quit_button]:
            button.update_text()
            button.update(screen=self.screen)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.update_mouse_position()
                if self.play_button.check_for_input(position=self.mouse_position):
                    Game(settings=self.settings, screen=self.screen).play_game()
                if self.options_button.check_for_input(position=self.mouse_position):
                    Options(settings=self.settings, screen=self.screen).options()
                if self.leaderboard_button.check_for_input(position=self.mouse_position):
                    Leaderboard(settings=self.settings, screen=self.screen).leaderboard()
                if self.quit_button.check_for_input(position=self.mouse_position):
                    pygame.quit()
                    sys.exit()

    def menu(self):
        while True:
            self.draw_default_background()
            self._draw_title()
            self._draw_buttons()
            self._check_events()
            pygame.display.flip()
