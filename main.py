import copy
import random
import sys
from typing import List, Optional

import pygame
from pygame.math import Vector2

WHITE = (255, 255, 255)
RED = (168, 50, 50)
GREEN = (175, 215, 70)
BLUE = (50, 145, 168)
SNAKE_WIDTH = 20
SNAKE_HEIGHT = 40
cell_size = 40
cell_number = 25


class Fruit:
    def __init__(self, fruit_forbidden_positions: List[Vector2]):
        self._x = random.randint(2, cell_number - 2)
        self._y = random.randint(2, cell_number - 2)
        self.position = Vector2(self._x, self._y)
        while self.position in fruit_forbidden_positions:
            self._x = random.randint(2, cell_number - 2)
            self._y = random.randint(2, cell_number - 2)
            self.position = Vector2(self._x, self._y)
        sprites = Sprite("assets/snake-graphics.png")
        self.apple_image = pygame.transform.scale(surface=sprites.get_sprite(0, 64 * 3, 64, 64),
                                                  size=(cell_size, cell_size))

    def draw_fruit(self, screen):
        position_cell_x = int(self.position.x * cell_size)
        position_cell_y = int(self.position.y * cell_size)
        fruit_rect = pygame.Rect(position_cell_x, position_cell_y, cell_size, cell_size)
        # apple = pygame.transform.scale(pygame.image.load("assets/fruit.png").convert_alpha(), (cell_size, cell_size))
        screen.blit(self.apple_image, fruit_rect)


class Sprite:
    def __init__(self, path):
        self.sprite = pygame.image.load(path).convert_alpha()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sprite, (0, 0), (x, y, width, height))
        sprite.set_colorkey((0, 0, 0))
        return sprite


class SnakeBlock:
    def __init__(self, position: Vector2, direction: Vector2, next_block: Optional['SnakeBlock'] = None,
                 previous_block: Optional['SnakeBlock'] = None):
        self.position = position
        self.direction = direction
        self.next_block = next_block
        self.previous_block = previous_block

    @property
    def tail(self):
        if self.next_block:
            return False
        return True

    @property
    def head(self):
        if self.previous_block:
            return False
        return True


class Snake:
    def __init__(self, direction: Vector2):

        position = Vector2(cell_number // 2, cell_number // 2)
        nexts = SnakeBlock(position=position - Vector2(1, 0), direction=direction)
        self.snake_body = SnakeBlock(position=position, direction=direction, next_block=nexts)
        self.snake_body.next_block.previous_block = self.snake_body
        self._next_direction: Vector2 = direction
        self._length: int = 1
        self.eat_fruit = False
        snake_sprites = Sprite("assets/snake-graphics.png")
        self.head_img = pygame.transform.scale(surface=snake_sprites.get_sprite(64 * 3, 64 * 0, 64, 64),
                                               size=(cell_size, cell_size))
        self.body_block_img = pygame.transform.scale(surface=snake_sprites.get_sprite(64 * 1, 64 * 0, 64, 64),
                                                     size=(cell_size, cell_size))
        self.body_turn_block_img = pygame.transform.scale(surface=snake_sprites.get_sprite(64 * 0, 64 * 0, 64, 64),
                                                          size=(cell_size, cell_size))
        self.tail_img = pygame.transform.scale(surface=snake_sprites.get_sprite(64 * 3, 64 * 2, 64, 64),
                                               size=(cell_size, cell_size))

    @property
    def snake_body_positions(self) -> List[Vector2]:
        block_positions = []
        block = self.snake_body
        while block is not None:
            block_positions.append(block.position)
            block = block.next_block
        return block_positions

    def draw_snake(self, screen):
        block_to_draw = self.snake_body
        while block_to_draw:
            position_cell_x = int(block_to_draw.position.x * cell_size)
            position_cell_y = int(block_to_draw.position.y * cell_size)
            if block_to_draw.head:
                body_block_img = self.head_img
                if self.snake_body.direction == Vector2(1, 0):
                    body_block_img = pygame.transform.rotate(body_block_img, 270)
                elif self.snake_body.direction == Vector2(-1, 0):
                    body_block_img = pygame.transform.rotate(body_block_img, 90)
                elif self.snake_body.direction == Vector2(0, 1):
                    body_block_img = pygame.transform.rotate(body_block_img, 180)
                else:
                    body_block_img = pygame.transform.rotate(body_block_img, 0)
            elif block_to_draw.tail:
                body_block_img = self.tail_img
                if block_to_draw.direction == Vector2(1, 0):
                    body_block_img = pygame.transform.rotate(body_block_img, 270)
                elif block_to_draw.direction == Vector2(-1, 0):
                    body_block_img = pygame.transform.rotate(body_block_img, 90)
                elif block_to_draw.direction == Vector2(0, 1):
                    body_block_img = pygame.transform.rotate(body_block_img, 180)
                else:
                    body_block_img = pygame.transform.rotate(body_block_img, 0)
            else:
                if block_to_draw.direction == block_to_draw.next_block.direction:
                    body_block_img = self.body_block_img
                    if block_to_draw.direction == Vector2(1, 0) or block_to_draw.direction == Vector2(-1, 0):
                        body_block_img = pygame.transform.rotate(body_block_img, 0)
                    else:
                        body_block_img = pygame.transform.rotate(body_block_img, 90)

                else:
                    body_turn_block_img = self.body_turn_block_img

                    if block_to_draw.next_block.direction == Vector2(1, 0) and block_to_draw.direction == Vector2(0, 1):
                        body_block_img = pygame.transform.rotate(body_turn_block_img, 270)
                    elif (block_to_draw.next_block.direction == Vector2(1, 0)
                          and block_to_draw.direction == Vector2(0, -1)):
                        body_block_img = pygame.transform.rotate(body_turn_block_img, 180)
                    elif (block_to_draw.next_block.direction == Vector2(-1, 0)
                          and block_to_draw.direction == Vector2(0, 1)):
                        body_block_img = pygame.transform.rotate(body_turn_block_img, 0)
                    elif (block_to_draw.next_block.direction == Vector2(-1, 0)
                          and block_to_draw.direction == Vector2(0, -1)):
                        body_block_img = pygame.transform.rotate(body_turn_block_img, 90)
                    elif (block_to_draw.next_block.direction == Vector2(0, 1)
                          and block_to_draw.direction == Vector2(1, 0)):
                        body_block_img = pygame.transform.rotate(body_turn_block_img, 90)
                    elif (block_to_draw.next_block.direction == Vector2(0, 1)
                          and block_to_draw.direction == Vector2(-1, 0)):
                        body_block_img = pygame.transform.rotate(body_turn_block_img, 180)
                    elif (block_to_draw.next_block.direction == Vector2(0, -1)
                          and block_to_draw.direction == Vector2(1, 0)):
                        body_block_img = pygame.transform.rotate(body_turn_block_img, 0)
                    else:
                        body_block_img = pygame.transform.rotate(body_turn_block_img, 270)

            screen.blit(body_block_img, (position_cell_x, position_cell_y))
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
        self._length += 1
        self.eat_fruit = False


class Game:
    def __init__(self):
        self.snake = Snake(Vector2(1, 0))
        self.fruit = Fruit(fruit_forbidden_positions=self.snake.snake_body_positions)
        self.score = 0
        self.game_over = False
        self.game_font = pygame.font.SysFont('comicsans', 25)
        self.background_tile_1 = pygame.image.load('assets/grass-pattern1.jpg')
        self.background_tile_2 = pygame.image.load('assets/grass-pattern2.jpg')

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
        self.draw_score(screen=screen)

    def check_collision(self):
        if self.fruit.position == self.snake.snake_body.position:
            self.snake.eat_fruit = True
            self.score += 1
            fruit_forbidden_positions = self.snake.snake_body_positions
            self.fruit = Fruit(fruit_forbidden_positions=fruit_forbidden_positions)
        self.check_snake_collision_with_boundary()
        self.check_snake_collision_with_itself()

    def check_snake_collision_with_itself(self):
        snake_head = self.snake.snake_body
        snake_block = self.snake.snake_body.next_block
        while snake_block and not snake_block.tail:
            if snake_head.position == snake_block.position:
                self.game_over = True
            snake_block = snake_block.next_block

    def check_snake_collision_with_boundary(self):
        if (not 0 <= self.snake.snake_body.position.x < cell_number
                or not 0 <= self.snake.snake_body.position.y < cell_number):
            self.game_over = True

    def draw_background(self, screen):
        for row in range(cell_number):
            if row % 2 == 0:
                for column in range(cell_number):
                    if column % 2 == 0:
                        grass_rect = pygame.transform.scale(surface=self.background_tile_1, size=(cell_size, cell_size))
                    else:
                        grass_rect = pygame.transform.scale(surface=self.background_tile_2, size=(cell_size, cell_size))
                    screen.blit(grass_rect, (row * cell_size, column * cell_size))
            else:
                for column in range(cell_number):
                    if column % 2 == 0:
                        grass_rect = pygame.transform.scale(surface=self.background_tile_2, size=(cell_size, cell_size))
                    else:
                        grass_rect = pygame.transform.scale(surface=self.background_tile_1, size=(cell_size, cell_size))
                    screen.blit(grass_rect, (row * cell_size, column * cell_size))

    def draw_score(self, screen):
        score_text = f'Score: {self.score}'
        score_surface = self.game_font.render(score_text, True, (56, 74, 12))
        score_surface.set_colorkey((0, 0, 0, 0))  # Set black color as transparent

        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))

        screen.blit(score_surface, score_rect)


def game_over(screen):
    pass


def play(screen):
    clock = pygame.time.Clock()
    screen_update = pygame.USEREVENT
    pygame.time.set_timer(screen_update, 100)

    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == screen_update:
                game.update()
            if event.type == pygame.KEYDOWN:
                game.change_direction(event=event)
                game.update()

        if game.game_over:
            pygame.time.delay(200)
            break
        if not game.game_over:
            game.draw_background(screen=screen)
            game.draw_elements(screen=screen)
        pygame.display.update()
        clock.tick(60)


class Button(pygame.sprite.Sprite):
    def __init__(self, image=None, pos=(0, 0), text_input="", font=None, base_color=(255, 255, 255),
                 hovering_color=(200, 200, 200)):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(center=pos) if self.image else pygame.Rect(pos[0], pos[1], 0, 0)
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.update_text()

    def update_text(self):
        color = self.hovering_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.base_color
        text = self.font.render(self.text_input, True, color)
        self.image = text
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, screen):
        screen.blit(self.image, self.rect)

    def check_for_input(self, position):
        return self.rect.collidepoint(position)


def get_font(size):
    return pygame.font.SysFont('comicsansms', size=size)


def main_menu():
    pygame.init()

    screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))

    pygame.display.set_caption('Menu')
    game_cover = pygame.transform.scale(surface=pygame.image.load('assets/snake-game-cover.jpg'),
                                        size=(cell_number * cell_size, cell_number * cell_size))
    while True:
        screen.blit(game_cover, (0, 0))

        menu_mouse_position = pygame.mouse.get_pos()

        menu_text = get_font(150).render('Menu', True, "#ebedbe")
        menu_rect = menu_text.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 6))

        play_button = Button(image=None,
                             pos=(cell_size * cell_number // 2, cell_size * cell_number // 6 * 2),
                             text_input="PLAY",
                             font=get_font(75),
                             base_color="#d7fcd4",
                             hovering_color="White"
                             )
        options_button = Button(image=None,
                                pos=(cell_size * cell_number // 2, cell_size * cell_number // 6 * 3),
                                text_input="OPTIONS",
                                font=get_font(75),
                                base_color="#d7fcd4",
                                hovering_color="White"
                                )
        quit_button = Button(image=None,
                             pos=(cell_size * cell_number // 2, cell_size * cell_number // 6 * 4),
                             text_input="QUIT",
                             font=get_font(75),
                             base_color="#d7fcd4",
                             hovering_color="White"
                             )
        screen.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.update_text()
            button.update(screen=screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(position=menu_mouse_position):
                    play(screen=screen)
                if options_button.check_for_input(position=menu_mouse_position):
                    print('options')
                if quit_button.check_for_input(position=menu_mouse_position):
                    print('quit')
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


if __name__ == '__main__':
    main_menu()
