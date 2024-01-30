import pygame
from pygame import Vector2

from game_settings import Settings


class Wall:

    def __init__(self, settings: Settings, start_position: Vector2, end_position: Vector2) -> None:
        self.settings = settings
        self.start_position = start_position
        self.end_position = end_position

    def draw(self, screen):
        wall_rect = pygame.Rect(self.start_position.x, self.start_position.y, self.end_position.x, self.end_position.y)
        screen.blit(wall_rect)
