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
    red: Path
    green: Path
    brown: Path


class Difficult(BaseModel):
    screen_update_time: int
    fps: int
    blocks: bool


class DifficultyMapping(BaseModel):
    easy: Difficult
    medium: Difficult
    hard: Difficult


class Settings:
    TILES = Tiles(
        grass=TilesType(
            tile_1='assets/grass-pattern1.jpg',
            tile_2='assets/grass-pattern2.jpg'
        ),
        stone=TilesType(
            tile_1='assets/stone-pattern1.jpg',
            tile_2='assets/stone-pattern2.jpg'
        ),
        dirt=TilesType(
            tile_1='assets/sand-pattern1.jpg',
            tile_2='assets/sand-pattern2.jpg'
        )
    )

    SNAKE_COLOR = SnakeColor(
        red=Path(path='assets/snake-graphics-red.png'),
        green=Path(path='assets/snake-graphics.png'),
        brown=Path(path='assets/snake-graphics-brown.png')
    )
    DIFFICULTY_MAPPING = DifficultyMapping(
        easy=Difficult(
            screen_update_time=200,
            fps=30,
            blocks=False
        ),
        medium=Difficult(
            screen_update_time=150,
            fps=45,
            blocks=False
        ),
        hard=Difficult(
            screen_update_time=100,
            fps=60,
            blocks=False
        )
    )

    def __init__(self):
        self.cell_size = 40
        self.cell_number = 25
        self.difficulty = 'easy'
        self.screen_update_time = 100
        self.fps = 60
        self.blocks = False

        self.update_difficulty()
        self.font = 'comicsansms'
        self.tile_type = 'grass'
        self.screen_delay_on_game_over = 1000
        self.darkness_mode = False
        self.snake_color = 'green'

    def update_darkness_mode(self, darkness_mode: bool):
        print('Darkness mode:', darkness_mode)
        self.darkness_mode = darkness_mode

    def update_difficulty(self, difficulty='easy'):
        self.difficulty = difficulty
        if self.difficulty == 'easy':
            difficult = self.DIFFICULTY_MAPPING.easy
        elif self.difficulty == 'medium':
            difficult = self.DIFFICULTY_MAPPING.easy
        else:
            difficult = self.DIFFICULTY_MAPPING.hard
        self.screen_update_time = difficult.screen_update_time
        self.fps = difficult.fps

    def get_tile_by_type(self) -> TilesType:
        if self.tile_type == 'grass':
            return self.TILES.grass
        if self.tile_type == 'stone':
            return self.TILES.stone
        if self.tile_type == 'dirt':
            return self.TILES.dirt

    def get_snake_color_path_by_type(self) -> str:
        if self.snake_color == 'green':
            return self.SNAKE_COLOR.green.path
        if self.snake_color == 'red':
            return self.SNAKE_COLOR.red.path
        if self.snake_color == 'brown':
            return self.SNAKE_COLOR.brown.path

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
