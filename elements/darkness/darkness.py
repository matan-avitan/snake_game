import pygame

from pygame import Vector2, Surface
from typing import List

from game_settings import Settings


class Darkness:
    DARKNESS_PATH = 'assets/darkness.jpg'
    DARKNESS_OFFSET = 3

    def __init__(self, settings: Settings, snake_position: Vector2) -> None:
        self.settings = settings
        self.snake_position = snake_position
        self.light = self._calculate_light()
        darkness_img = pygame.image.load(self.DARKNESS_PATH).convert_alpha()
        self.darkness_img = pygame.transform.scale(surface=darkness_img, size=self.settings.tile_dimensions)
        self.light_img = pygame.transform.scale(surface=darkness_img, size=self.settings.tile_dimensions)
        self.light_img.set_colorkey((0, 0, 0))

    def update_snake_position(self, snake_position: Vector2) -> None:
        if snake_position != self.snake_position:
            self.snake_position = snake_position
            self.light = self._calculate_light()

    def _calculate_light(self) -> List[Vector2]:
        lights = []
        for light_x in range(int(self.snake_position.x) - self.DARKNESS_OFFSET,
                             int(self.snake_position.x) + self.DARKNESS_OFFSET + 1):
            for light_y in range(int(self.snake_position.y) - self.DARKNESS_OFFSET,
                                 int(self.snake_position.y) + self.DARKNESS_OFFSET + 1):
                if not (light_x < 0 or light_y < 0 or light_x >= self.settings.cell_number
                        or light_y >= self.settings.cell_number):
                    lights.append(Vector2(light_x, light_y))
        return lights

    def _draw_darkness(self, screen: Surface) -> None:
        for block_x in range(self.settings.cell_number):
            for block_y in range(self.settings.cell_number):
                self.darkness_img.set_alpha(256)
                block_to_draw = Vector2(block_x, block_y)
                if block_to_draw not in self.light:
                    position_cell_x = int(block_to_draw.x * self.settings.cell_size)
                    position_cell_y = int(block_to_draw.y * self.settings.cell_size)
                    screen.blit(self.darkness_img, (position_cell_x, position_cell_y))

    def _draw_lights(self, screen: Surface) -> None:
        for block_to_draw in self.light:
            position_cell_x = int(block_to_draw.x * self.settings.cell_size)
            position_cell_y = int(block_to_draw.y * self.settings.cell_size)
            light_distance = Vector2(abs(self.snake_position.x - block_to_draw.x),
                                     abs(self.snake_position.y - block_to_draw.y))
            if light_distance.x == 0 and light_distance.y == 0:
                self.light_img.set_alpha(0)
            elif light_distance.x <= 1 and light_distance.y <= 1:
                self.light_img.set_alpha(60)
            elif light_distance.x <= 2 and light_distance.y <= 2:
                self.light_img.set_alpha(120)
            elif light_distance.x <= 3 and light_distance.y <= 3:
                self.light_img.set_alpha(180)
            screen.blit(self.light_img, (position_cell_x, position_cell_y))

    def draw(self, screen: Surface) -> None:
        if self.settings.darkness_mode:
            self._draw_darkness(screen=screen)
            self._draw_lights(screen=screen)
