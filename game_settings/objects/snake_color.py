from pydantic import BaseModel


class Path(BaseModel):
    path: str


class SnakeColor(BaseModel):
    red: Path
    green: Path
    brown: Path


SNAKE_COLOR = SnakeColor(
    red=Path(path='assets/snake-graphics-red.png'),
    green=Path(path='assets/snake-graphics.png'),
    brown=Path(path='assets/snake-graphics-brown.png')
)
