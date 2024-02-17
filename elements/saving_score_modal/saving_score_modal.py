import pygame
from pygame import Surface

from game_settings import Settings


class SavingScoreModal:
    def __init__(self, settings: Settings, score: int) -> None:
        self.settings = settings
        self.score = score
        self.name = None

    def update_name(self, name: str):
        self.name = name

    def _draw_text(self, screen: Surface, text: str, position: tuple, font_size: int, color: tuple):
        font = self.settings.get_font(size=font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        screen.blit(text_surface, text_rect)

    def _draw_input_box(self, screen: Surface, name: str):
        font = self.settings.get_font(size=32)
        input_rect = pygame.Rect(0, 0, 300, 40)
        input_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 + 50)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)
        text_surface = font.render(name, True, (255, 255, 255))
        text_rect = text_surface.get_rect(left=input_rect.left + 5, centery=input_rect.centery)
        screen.blit(text_surface, text_rect)

    def draw_score_input_modal(self, screen: Surface):
        name = ''
        font_size_large = 72
        font_size_normal = 32
        font_color_red = (255, 0, 0)
        font_color_white = (255, 255, 255)

        input_active = True
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

            screen.fill((30, 30, 30))
            self._draw_text(screen, "Game Over",
                            (self.settings.screen_width // 2, self.settings.screen_height // 2 - 200), font_size_large,
                            font_color_red)
            self._draw_text(screen, f"You got {self.score} points",
                            (self.settings.screen_width // 2, self.settings.screen_height // 2 - 50), font_size_normal,
                            font_color_white)
            self._draw_text(screen, "Please enter your name:",
                            (self.settings.screen_width // 2, self.settings.screen_height // 2), font_size_normal,
                            font_color_white)
            self._draw_input_box(screen, name)
            pygame.display.flip()

        self.settings.update_scoreboard(score=self.score, name=name)

    def _save_score(self, name, score):
        with open("scores.txt", "a") as file:
            file.write(f"{name}: {score}\n")
