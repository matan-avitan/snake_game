import sys
import pygame
from pygame import Surface, SRCALPHA
from elements import Button
from game_settings import Settings


class Leaderboard:
    MENU_COVER_PATH = 'assets/snake-game-cover.jpg'

    def __init__(self, settings: Settings, screen: Surface):
        self.settings = settings
        self.screen = screen
        self.back = False
        self.game_cover = pygame.transform.scale(surface=pygame.image.load(self.MENU_COVER_PATH),
                                                 size=self.settings.screen_dimensions).convert_alpha()
        self.game_cover.fill((255, 255, 255, 180), None, pygame.BLEND_RGBA_MULT)  # Increase opacity

    def draw_top_scores(self) -> None:
        font = self.settings.get_font(size=32)
        x_offset = self.settings.screen_width // 2
        y_offset = 50
        line_spacing = 40

        background_surface = pygame.Surface((self.settings.screen_width, self.settings.screen_height), SRCALPHA)
        background_surface.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(background_surface, (0, 0))

        for level, scores in self.settings.scoreboard.dict().items():
            if level == "easy":
                color = (0, 255, 0)
            elif level == "medium":
                color = (255, 255, 0)
            else:
                color = (255, 0, 0)

            text_surface = font.render(f"Top 5 {level.capitalize()} Scores:", True, color)
            text_rect = text_surface.get_rect(center=(x_offset, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += line_spacing

            for scoreline in scores[:5]:
                text_surface = font.render(f"{scoreline['name']}: {scoreline['score']}", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(x_offset, y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += line_spacing

            y_offset += line_spacing

    def _get_button(self, text, y_position, x_position=None, is_selected=False, value=None) -> Button:
        color = "blue" if is_selected else "black"
        x_position = self.settings.screen_width // 2 if not x_position else x_position
        return Button(image=None,
                      pos=(x_position, self.settings.screen_height // 9 * y_position),
                      text_input=text,
                      font=self.settings.get_font(size=50),
                      base_color=color,
                      hovering_color="white",
                      value=value
                      )

    def leaderboard(self) -> None:
        while True:
            options_mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.game_cover, (0, 0))
            options_back = self._get_button(text="Back", y_position=8, is_selected=False)
            options_back.update_text()
            options_back.update(self.screen)
            self.draw_top_scores()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if options_back.check_for_input(options_mouse_pos):
                        self.back = True
            if self.back:
                break
