from typing import Optional

from pygame import Vector2


class SnakeBlock:
    def __init__(self, position: Vector2, direction: Vector2, next_block: Optional['SnakeBlock'] = None,
                 previous_block: Optional['SnakeBlock'] = None):
        self.position = position
        self.direction = direction
        self.next_block = next_block
        self.previous_block = previous_block

    @property
    def tail(self) -> bool:
        if self.next_block:
            return False
        return True

    @property
    def head(self) -> bool:
        if self.previous_block:
            return False
        return True
