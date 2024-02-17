import json
from typing import Tuple, List

import pygame

from game_settings.objects import ScoreBoard, ScoreLine, DIFFICULTY_MAPPING, SCORE_BOARD_JSON_PATH, TilesType, TILES, \
    SNAKE_COLOR


class Settings:

    def __init__(self):
        # screen:
        self.cell_size = 40
        self.cell_number = 25
        self.screen_update_time = 100
        self.fps = 60
        self.screen_delay_on_game_over = 1000
        self.game_font = 'comicsansms'

        # options
        self.difficulty = 'easy'
        self.update_difficulty()
        self.tile_type = 'grass'
        self.darkness_mode = False
        self.snake_color = 'green'

        # scoreboard
        self.scoreboard: ScoreBoard = self._read_scoreboard_from_json()

    def update_scoreboard(self, score: int, name: str):
        new_scoreline = ScoreLine(score=score, name=name)
        if self.difficulty == 'easy':
            self.scoreboard.easy.append(new_scoreline)
        elif self.difficulty == 'medium':
            self.scoreboard.medium.append(new_scoreline)
        else:
            self.scoreboard.hard.append(new_scoreline)

        setattr(self.scoreboard, self.difficulty,
                sorted(getattr(self.scoreboard, self.difficulty), key=lambda x: x.score, reverse=True))
        self._save_scoreboard_to_json()

    @staticmethod
    def _read_scoreboard_from_json() -> ScoreBoard:
        try:
            with open(SCORE_BOARD_JSON_PATH, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {
                'easy': [],
                'medium': [],
                'hard': []
            }
            with open(SCORE_BOARD_JSON_PATH, 'w') as file:
                json.dump(data, file, indent=4)
        return ScoreBoard(**data)

    def _save_scoreboard_to_json(self):
        with open(SCORE_BOARD_JSON_PATH, 'w') as file:
            json.dump(self.scoreboard.dict(), file, indent=4)

    def update_darkness_mode(self, darkness_mode: bool):
        print('Darkness mode:', darkness_mode)
        self.darkness_mode = darkness_mode

    def update_difficulty(self, difficulty='easy'):
        self.difficulty = difficulty
        if self.difficulty == 'easy':
            difficult = DIFFICULTY_MAPPING.easy
        elif self.difficulty == 'medium':
            difficult = DIFFICULTY_MAPPING.easy
        else:
            difficult = DIFFICULTY_MAPPING.hard
        self.screen_update_time = difficult.screen_update_time
        self.fps = difficult.fps

    def get_tile_by_type(self) -> TilesType:
        if self.tile_type == 'grass':
            return TILES.grass
        if self.tile_type == 'stone':
            return TILES.stone
        if self.tile_type == 'sand':
            return TILES.sand

    def get_snake_color_path_by_type(self) -> str:
        if self.snake_color == 'green':
            return SNAKE_COLOR.green.path
        if self.snake_color == 'red':
            return SNAKE_COLOR.red.path
        if self.snake_color == 'brown':
            return SNAKE_COLOR.brown.path

    def get_font(self, size):
        return pygame.font.SysFont(self.game_font, size=size)

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
