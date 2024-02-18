import copy
from typing import List

from pygame import Vector2, Surface, transform

from elements.snake.snake_block import SnakeBlock
from game_settings import Settings
from utils import SpriteExtractor


class Snake:
    IMG_ROW = 3
    IMG_COL = 0
    WIDTH = 64
    HEIGHT = 64

    def __init__(self, settings: Settings, direction: Vector2):
        self.settings = settings
        self.block_size = (self.settings.cell_size, self.settings.cell_size)
        self._next_direction: Vector2 = direction
        self.snake_body = None
        self._init_snake()
        self.eat_fruit = False
        self.snake_sprites = SpriteExtractor(self.settings.get_snake_color_path_by_type())

    def _init_snake(self):
        position = Vector2(self.settings.cell_number // 2, self.settings.cell_number // 2)
        head = SnakeBlock(position=position, direction=self._next_direction)
        body = SnakeBlock(position=position - self._next_direction, direction=self._next_direction, previous_block=head)
        tail = SnakeBlock(position=position - 2 * self._next_direction,
                          direction=self._next_direction,
                          previous_block=body)
        body.next_block = tail
        head.next_block = body
        self.snake_body = head

    @property
    def head_img(self) -> Surface:
        surface = self.snake_sprites.get_sprite(x=self.WIDTH * 3, y=self.HEIGHT * 0, height=self.HEIGHT,
                                                width=self.WIDTH)
        return transform.scale(surface=surface, size=self.block_size)

    @property
    def body_block_img(self) -> Surface:
        surface = self.snake_sprites.get_sprite(x=self.WIDTH * 1, y=self.HEIGHT * 0, height=self.HEIGHT,
                                                width=self.WIDTH)
        return transform.scale(surface=surface, size=self.block_size)

    @property
    def body_turn_block_img(self) -> Surface:
        surface = self.snake_sprites.get_sprite(x=self.WIDTH * 0, y=self.HEIGHT * 0, height=self.HEIGHT,
                                                width=self.WIDTH)
        return transform.scale(surface=surface, size=self.block_size)

    @property
    def tail_img(self) -> Surface:
        surface = self.snake_sprites.get_sprite(x=self.WIDTH * 3, y=self.HEIGHT * 2, height=self.HEIGHT,
                                                width=self.WIDTH)
        return transform.scale(surface=surface, size=self.block_size)

    @property
    def snake_body_positions(self) -> List[Vector2]:
        block_positions = []
        block = self.snake_body
        while block is not None:
            block_positions.append(block.position)
            block = block.next_block
        return block_positions

    def _draw_head(self) -> Surface:
        block_img = self.head_img
        if self.snake_body.direction == Vector2(1, 0):
            return transform.rotate(block_img, 270)
        elif self.snake_body.direction == Vector2(-1, 0):
            return transform.rotate(block_img, 90)
        elif self.snake_body.direction == Vector2(0, 1):
            return transform.rotate(block_img, 180)
        else:
            return transform.rotate(block_img, 0)

    def _draw_tail(self, block_to_draw: SnakeBlock) -> Surface:
        block_img = self.tail_img
        if block_to_draw.direction == Vector2(1, 0):
            return transform.rotate(block_img, 270)
        elif block_to_draw.direction == Vector2(-1, 0):
            return transform.rotate(block_img, 90)
        elif block_to_draw.direction == Vector2(0, 1):
            return transform.rotate(block_img, 180)
        else:
            return transform.rotate(block_img, 0)

    def _draw_straight_body(self, block_to_draw: SnakeBlock) -> Surface:
        block_img = self.body_block_img
        if block_to_draw.direction == Vector2(1, 0) or block_to_draw.direction == Vector2(-1, 0):
            return transform.rotate(block_img, 0)
        else:
            return transform.rotate(block_img, 90)

    def _draw_turn_body(self, block_to_draw: SnakeBlock) -> Surface:
        block_img = self.body_turn_block_img
        next_block_direction = block_to_draw.next_block.direction
        block_direction = block_to_draw.direction
        if next_block_direction == Vector2(1, 0) and block_direction == Vector2(0, 1):
            return transform.rotate(surface=block_img, angle=270)
        elif next_block_direction == Vector2(1, 0) and block_direction == Vector2(0, -1):
            return transform.rotate(surface=block_img, angle=180)
        elif next_block_direction == Vector2(-1, 0) and block_direction == Vector2(0, 1):
            return transform.rotate(surface=block_img, angle=0)
        elif next_block_direction == Vector2(-1, 0) and block_direction == Vector2(0, -1):
            return transform.rotate(surface=block_img, angle=90)
        elif next_block_direction == Vector2(0, 1) and block_direction == Vector2(1, 0):
            return transform.rotate(surface=block_img, angle=90)
        elif next_block_direction == Vector2(0, 1) and block_direction == Vector2(-1, 0):
            return transform.rotate(surface=block_img, angle=180)
        elif next_block_direction == Vector2(0, -1) and block_direction == Vector2(1, 0):
            return transform.rotate(surface=block_img, angle=0)
        else:
            return transform.rotate(block_img, 270)

    def draw(self, screen):
        block_to_draw = self.snake_body
        while block_to_draw:
            position_cell_x = int(block_to_draw.position.x * self.settings.cell_size)
            position_cell_y = int(block_to_draw.position.y * self.settings.cell_size)
            if block_to_draw.head:
                block_img = self._draw_head()
            elif block_to_draw.tail:
                block_img = self._draw_tail(block_to_draw=block_to_draw)
            else:
                if block_to_draw.direction == block_to_draw.next_block.direction:
                    block_img = self._draw_straight_body(block_to_draw=block_to_draw)
                else:
                    block_img = self._draw_turn_body(block_to_draw=block_to_draw)
            screen.blit(block_img, (position_cell_x, position_cell_y))
            block_to_draw = block_to_draw.next_block

    def update_direction(self, direction):
        # check don't try to do reverse
        if direction.x * self._next_direction.x != -1 and direction.y * self._next_direction.y != -1:
            self._next_direction = direction

    def move(self):
        if self.eat_fruit:
            self.add_block()
        else:
            new_direction = self._next_direction
            self.snake_body.direction = new_direction
            next_block_direction = self.snake_body.direction
            self.snake_body.position = self.snake_body.position + self.snake_body.direction
            snake_block = self.snake_body.next_block

            while snake_block is not None:
                snake_block.position = snake_block.position + snake_block.direction
                temp_direction = snake_block.direction
                snake_block.direction = next_block_direction
                next_block_direction = temp_direction
                snake_block = snake_block.next_block

    def add_block(self):
        new_head_position = self.snake_body.position + self.snake_body.direction
        prev_blocks = copy.deepcopy(self.snake_body)
        new_snake_head = SnakeBlock(position=new_head_position, direction=self.snake_body.direction,
                                    next_block=prev_blocks)
        new_snake_head.next_block.previous_block = new_snake_head
        self.snake_body = new_snake_head
        self.eat_fruit = False
