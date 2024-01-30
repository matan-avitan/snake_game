import pygame
from pygame import Vector2

from game_settings import Settings


class Wall:
    WALL_PATH = "assets/wall.jpg"

    def __init__(self, settings: Settings, start_position: Vector2, end_position: Vector2) -> None:
        self.settings = settings
        self.start_position = start_position
        self.end_position = end_position
        wall_img = pygame.image.load(self.WALL_PATH).convert_alpha()
        self.wall_img = pygame.transform.scale(surface=wall_img, size=self.settings.tile_dimensions)
        self.tiles = []
        if self.start_position.x == self.end_position.x:
            for y in range(int(self.start_position.y), int(self.end_position.y) + 1):
                self.tiles.append(Vector2(self.start_position.x, y))
        elif self.start_position.y == self.end_position.y:
            for x in range(int(self.start_position.x), int(self.end_position.x) + 1):
                self.tiles.append(Vector2(x, self.start_position.y))

    def draw(self, screen):
        for tile in self.tiles:
            position_cell_x = int(tile.x * self.settings.cell_size)
            position_cell_y = int(tile.y * self.settings.cell_size)
            screen.blit(self.wall_img, (position_cell_x, position_cell_y))
