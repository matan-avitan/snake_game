import random
from typing import List

import pygame
from pygame.math import Vector2

WHITE = (255, 255, 255)
RED = (168, 50, 50)
GREEN = (175, 215, 70)
BLUE = (50, 145, 168)
SNAKE_WIDTH = 20
SNAKE_HEIGHT = 40
cell_size = 40
cell_number = 20


class Fruit:
    def __init__(self):
        self._x = random.randint(0, cell_number - 1)
        self._y = random.randint(0, cell_number - 1)
        self.position = Vector2(self._x, self._y)

    def draw_fruit(self, screen):
        position_cell_x = int(self.position.x * cell_size)
        position_cell_y = int(self.position.y * cell_size)
        circle_center = (position_cell_x + cell_size // 2, position_cell_y + cell_size // 2)
        circle_radius = cell_size // 2

        pygame.draw.circle(screen, RED, circle_center, circle_radius)


class Snake:
    def __init__(self, direction: Vector2):
        self.body: List[Vector2] = [Vector2(cell_number // 2, cell_number // 2)]
        self.head = self.body[0]
        self._direction: Vector2 = direction
        self.eat_fruit = False

    def draw_snake(self, screen):
        for block in self.body:
            position_cell_x = int(block.x * cell_size)
            position_cell_y = int(block.y * cell_size)
            block_rect = pygame.Rect(position_cell_x, position_cell_y, cell_size, cell_size)
            pygame.draw.rect(screen, BLUE, block_rect)

    def update_direction(self, direction):
        # check don't try to do reverse
        if direction.x * self._direction.x != -1 and direction.y * self._direction.y != -1:
            self._direction = direction

    def move(self):
        if self.eat_fruit:
            self.add_block()
        elif self._direction != Vector2(0, 0):
            self.head = self.head + self._direction
            self.body = [self.head, *self.body[:-1]]

    def add_block(self):
        self.head = self.head + self._direction
        self.body = [self.head, *self.body[:]]
        self.eat_fruit = False


class Game:
    def __init__(self):
        self.snake = Snake(Vector2(0, 0))
        self.fruit = Fruit()
        self.game_over = False

    def update(self):
        self.snake.move()
        self.check_collision()

    def change_direction(self, event):
        if event.key == pygame.K_LEFT:
            self.snake.update_direction(Vector2(-1, 0))
        if event.key == pygame.K_RIGHT:
            self.snake.update_direction(Vector2(1, 0))
        if event.key == pygame.K_UP:
            self.snake.update_direction(Vector2(0, -1))
        if event.key == pygame.K_DOWN:
            self.snake.update_direction(Vector2(0, 1))

    def draw_elements(self, screen):
        self.fruit.draw_fruit(screen=screen)
        self.snake.draw_snake(screen=screen)

    def check_collision(self):
        if self.fruit.position == self.snake.head:
            self.snake.eat_fruit = True
            self.fruit = Fruit()
        self.check_snake_collision_with_boundary()
        self.check_snake_collision_with_itself()

    def check_snake_collision_with_itself(self):
        if self.snake.head in self.snake.body[1:]:
            self.game_over = True

    def check_snake_collision_with_boundary(self):
        if not 0 <= self.snake.head.x < cell_number or not 0 <= self.snake.head.y < cell_number:
            self.game_over = True


def draw_screen(screen):
    screen.fill(WHITE)


def run():
    pygame.init()

    screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
    clock = pygame.time.Clock()
    screen_update = pygame.USEREVENT
    game = Game()
    pygame.time.set_timer(screen_update, 150)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == screen_update:
                game.update()
            if event.type == pygame.KEYDOWN:
                game.change_direction(event=event)
        if game.game_over:
            break
        screen.fill(GREEN)
        game.draw_elements(screen=screen)
        pygame.display.update()
        clock.tick(60)
    run()
    # draw_screen(screen=screen)


if __name__ == '__main__':
    run()
