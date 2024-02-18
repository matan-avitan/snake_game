import random
from typing import List

import pygame
from pygame import Vector2

from game_settings import Settings
from utils import SpriteExtractor, resource_path


class Fruit:
    FRUIT_IMG_PATH = "assets/snake-graphics.png"
    IMG_ROW = 3
    IMG_COL = 0
    WIDTH = 64
    HEIGHT = 64

    def __init__(self, settings: Settings, fruit_forbidden_positions: List[Vector2]):
        self.settings = settings
        self._choose_random_location()
        while self.position in fruit_forbidden_positions:
            self._choose_random_location()
        self._update_fruit_image()

    def _update_fruit_image(self):
        sprites = SpriteExtractor(resource_path(self.FRUIT_IMG_PATH))
        fruit_surface = sprites.get_sprite(x=self.IMG_COL * self.WIDTH, y=self.IMG_ROW * self.HEIGHT, width=self.WIDTH,
                                           height=self.HEIGHT)
        self.apple_image = pygame.transform.scale(
            surface=fruit_surface,
            size=(self.settings.cell_size, self.settings.cell_size))

    def _choose_random_location(self):
        self._x = random.randint(2, self.settings.cell_number - 3)
        self._y = random.randint(2, self.settings.cell_number - 3)
        self.position = Vector2(self._x, self._y)

    def draw(self, screen):
        position_cell_x = int(self.position.x * self.settings.cell_size)
        position_cell_y = int(self.position.y * self.settings.cell_size)
        fruit_rect = pygame.Rect(position_cell_x, position_cell_y, self.settings.cell_size, self.settings.cell_size)
        screen.blit(self.apple_image, fruit_rect)
