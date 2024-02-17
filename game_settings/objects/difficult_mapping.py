from pydantic import BaseModel


class Difficult(BaseModel):
    screen_update_time: int
    fps: int
    blocks: bool


class DifficultyMapping(BaseModel):
    easy: Difficult
    medium: Difficult
    hard: Difficult


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
