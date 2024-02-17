import sys

import pygame
from pygame import SRCALPHA

from elements import Button
from game_settings import Settings
from screens.game.game import Game
from screens.leaderboard.leaderboard import Leaderboard
from screens.options.options import Options


class Menu:
    MENU_COVER_PATH = 'assets/snake-game-cover.jpg'

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.screen_dimensions)
        pygame.display.set_caption('Snake Game')
        self.game_cover = pygame.transform.scale(surface=pygame.image.load(self.MENU_COVER_PATH),
                                                 size=self.settings.screen_dimensions)
        self.game_cover.fill((255, 255, 255, 180), None, pygame.BLEND_RGBA_MULT)  # Increase opacity

    def _get_font(self, size):
        return pygame.font.SysFont(self.settings.game_font, size=size)

    def _get_button(self, text, y_position) -> Button:
        return Button(image=None,
                      pos=(self.settings.screen_width // 2, self.settings.screen_height // 6 * y_position),
                      text_input=text,
                      font=self.settings.get_font(size=75),
                      base_color="#d7fcd4",
                      hovering_color="White"
                      )

    def menu(self):
        while True:
            self.screen.blit(self.game_cover, (0, 0))
            background_surface = pygame.Surface((self.settings.screen_width, self.settings.screen_height), SRCALPHA)
            background_surface.fill((0, 0, 0, 128))  # Semi-transparent black
            self.screen.blit(background_surface, (0, 0))
            menu_mouse_position = pygame.mouse.get_pos()
            menu_text = self.settings.get_font(size=150).render('Menu', True, "#ebedbe")
            menu_rect = menu_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 6))

            play_button = self._get_button(text="Play", y_position=2)
            options_button = self._get_button(text="Options", y_position=3)
            leaderboard_button = self._get_button(text="Leader Board", y_position=4)
            quit_button = self._get_button(text="Quit", y_position=5)

            self.screen.blit(menu_text, menu_rect)

            for button in [play_button, options_button, leaderboard_button, quit_button]:
                button.update_text()
                button.update(screen=self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.check_for_input(position=menu_mouse_position):
                        Game(settings=self.settings, screen=self.screen).play_game()
                    if options_button.check_for_input(position=menu_mouse_position):
                        Options(settings=self.settings, screen=self.screen).options()
                    if leaderboard_button.check_for_input(position=menu_mouse_position):
                        Leaderboard(settings=self.settings, screen=self.screen).leaderboard()
                    if quit_button.check_for_input(position=menu_mouse_position):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
