from typing import Tuple

from pydantic import BaseModel


class TilesType(BaseModel):
    tile_1: str
    tile_2: str


class Tiles(BaseModel):
    grass: TilesType
    stone: TilesType
    dirt: TilesType


class Path(BaseModel):
    path: str


class SnakeColor(BaseModel):
    pass


class Settings:
    TILES = Tiles(
        grass=TilesType(
            tile_1='assets/grass-pattern1.jpg',
            tile_2='assets/grass-pattern2.jpg'
        ),
        stone=TilesType(
            tile_1='assets/grass-pattern1.jpg',
            tile_2='assets/grass-pattern2.jpg'
        ),
        dirt=TilesType(
            tile_1='assets/grass-pattern1.jpg',
            tile_2='assets/grass-pattern2.jpg'
        )
    )

    def __init__(self):
        self.cell_size = 40
        self.cell_number = 25
        self.level = 'Easy'
        self.font = 'comicsansms'
        self.tile_type = 'grass'
        self.screen_update_time = 100
        self.screen_delay_on_game_over = 200
        self.fps = 60
        self.snake_color = 'green'

    def get_tile_by_type(self) -> TilesType:
        if self.tile_type == 'grass':
            return self.TILES.grass
        if self.tile_type == 'stone':
            return self.TILES.stone
        if self.tile_type == 'dirt':
            return self.TILES.dirt

    @property
    def tile_dimensions(self) -> Tuple[int, int]:
        return self.cell_size, self.cell_size

    @property
    def screen_width(self) -> int:
        return self.cell_size * self.cell_number

    @property
    def screen_height(self) -> int:
        return self.cell_size * self.cell_number

    @property
    def screen_dimensions(self) -> Tuple[int, int]:
        return self.screen_width, self.screen_height

    def change_cell_size(self, cell_size) -> None:
        self.cell_size = cell_size

    def change_cell_number(self, cell_number) -> None:
        self.cell_number = cell_number
