from typing import List

from pydantic import BaseModel


class ScoreLine(BaseModel):
    score: int
    name: str


class ScoreBoard(BaseModel):
    easy: List[ScoreLine]
    medium: List[ScoreLine]
    hard: List[ScoreLine]

SCORE_BOARD_JSON_PATH = 'scoreboard.json'
