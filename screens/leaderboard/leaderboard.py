import sys
import pygame
from pygame import Surface, SRCALPHA
from elements import Button
from game_settings import Settings
from screens.base_screen import BaseScreen


class Leaderboard(BaseScreen):

    def __init__(self, settings: Settings, screen: Surface):
        super().__init__(settings=settings, screen=screen)
        self.back = False
        self.font = self.settings.get_font(size=32)
        self.options_back = self._get_button(text="Back", y_position=5.5)

    @staticmethod
    def get_font_color_by_difficulty(difficult: str) -> str:
        if difficult == "easy":
            color = 'green'
        elif difficult == "medium":
            color = 'yellow'
        else:  # hard
            color = 'red'
        return color

    def draw_title(self, difficult: str, color: str, x_offset: int, y_offset: int):
        text_surface = self.font.render(f"Top 5 {difficult.capitalize()} Scores:", True, color)
        text_rect = text_surface.get_rect(center=(x_offset, y_offset))
        self.screen.blit(text_surface, text_rect)

    def draw_score(self, scoreline: dict, x_offset: int, y_offset: int):
        text_surface = self.font.render(f"{scoreline['name']}: {scoreline['score']}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x_offset, y_offset))
        self.screen.blit(text_surface, text_rect)

    def draw_top_scores(self) -> None:
        x_offset = self.settings.screen_width // 2
        y_offset = 50
        line_spacing = 40

        for difficult, scores in self.settings.scoreboard.dict().items():
            color = self.get_font_color_by_difficulty(difficult=difficult)
            self.draw_title(difficult=difficult, color=color, x_offset=x_offset, y_offset=y_offset)
            y_offset += line_spacing

            for scoreline in scores[:5]:
                self.draw_score(scoreline=scoreline, x_offset=x_offset, y_offset=y_offset)
                y_offset += line_spacing

            y_offset += line_spacing

    def draw_back_option(self):
        self.options_back = self._get_button(text="Back", y_position=5.5)
        self.options_back.update_text()
        self.options_back.update(self.screen)

    def check_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if self.options_back.check_for_input(self.mouse_position):
                    self.back = True

    def leaderboard(self) -> None:
        while True:
            self.update_mouse_position()
            self.draw_default_background()
            self.draw_back_option()
            self.draw_top_scores()
            pygame.display.flip()
            self.check_for_events()
            if self.back:
                break
