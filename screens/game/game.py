import pygame
from pygame import Vector2, Surface

from elements import Snake, Fruit, Wall, Darkness, SavingScoreModal
from game_settings import Settings
from screens.base_screen import BaseScreen
from utils import resource_path


class Game(BaseScreen):
    def __init__(self, settings: Settings, screen: Surface):
        super().__init__(settings=settings, screen=screen)
        self.snake = Snake(settings=self.settings, direction=Vector2(1, 0))
        self.fruit = Fruit(settings=self.settings, fruit_forbidden_positions=self.snake.snake_body_positions)
        self.score = 0
        self.darkness = Darkness(settings=self.settings, snake_position=self.snake.snake_body.position)
        self.game_over = False
        self.background_tile_1 = pygame.image.load(resource_path(self.settings.get_tile_by_type().tile_1))
        self.background_tile_2 = pygame.image.load(resource_path(self.settings.get_tile_by_type().tile_2))
        self.border_height_left = Wall(settings=self.settings, start_position=Vector2(0, 0),
                                       end_position=Vector2(0, self.settings.cell_number - 1))
        self.border_width_up = Wall(settings=self.settings, start_position=Vector2(0, 0),
                                    end_position=Vector2(self.settings.cell_number - 1, 0))
        self.border_height_right = Wall(settings=self.settings,
                                        start_position=Vector2(self.settings.cell_number - 1, 0),
                                        end_position=Vector2(self.settings.cell_number - 1,
                                                             self.settings.cell_number - 1))
        self.border_width_down = Wall(settings=self.settings, start_position=Vector2(0, self.settings.cell_number - 1),
                                      end_position=Vector2(self.settings.cell_number - 1,
                                                           self.settings.cell_number - 1))
        self.screen_update = pygame.USEREVENT

    def _update(self):
        self.snake.move()
        self._check_collision()

    def _change_direction(self, event):
        if event.key == pygame.K_LEFT:
            self.snake.update_direction(Vector2(-1, 0))
        if event.key == pygame.K_RIGHT:
            self.snake.update_direction(Vector2(1, 0))
        if event.key == pygame.K_UP:
            self.snake.update_direction(Vector2(0, -1))
        if event.key == pygame.K_DOWN:
            self.snake.update_direction(Vector2(0, 1))

    def _draw_elements(self):
        self._draw_background()
        self.fruit.draw(screen=self.screen)
        self.snake.draw(screen=self.screen)
        self._draw_border()
        self.darkness.draw(screen=self.screen)
        self._draw_score()

    def _check_collision(self):
        if self.fruit.position == self.snake.snake_body.position:
            self.snake.eat_fruit = True
            self.score += 1
            fruit_forbidden_positions = self.snake.snake_body_positions
            self.fruit = Fruit(settings=self.settings, fruit_forbidden_positions=fruit_forbidden_positions)
        self._check_snake_collision_with_boundary()
        self._check_snake_collision_with_itself()

    def _check_snake_collision_with_itself(self):
        snake_head = self.snake.snake_body
        snake_block = self.snake.snake_body.next_block
        while snake_block and not snake_block.tail:
            if snake_head.position == snake_block.position:
                self.game_over = True
            snake_block = snake_block.next_block

    def _check_snake_collision_with_boundary(self):
        if (not 1 <= self.snake.snake_body.position.x < self.settings.cell_number - 1
                or not 1 <= self.snake.snake_body.position.y < self.settings.cell_number - 1):
            self.game_over = True

    def _get_tile_1(self):
        return pygame.transform.scale(surface=self.background_tile_1,
                                      size=self.settings.tile_dimensions)

    def _get_tile_2(self):
        return pygame.transform.scale(surface=self.background_tile_2,
                                      size=self.settings.tile_dimensions)

    def _draw_background(self):
        for row in range(self.settings.cell_number):
            if row % 2 == 0:
                for column in range(self.settings.cell_number):
                    tile_rect = self._get_tile_1() if column % 2 == 0 else self._get_tile_2()
                    self.screen.blit(source=tile_rect,
                                     dest=(row * self.settings.cell_size, column * self.settings.cell_size))
            else:
                for column in range(self.settings.cell_number):
                    tile_rect = self._get_tile_2() if column % 2 == 0 else self._get_tile_1()
                    self.screen.blit(source=tile_rect,
                                     dest=(row * self.settings.cell_size, column * self.settings.cell_size))

    def _draw_score(self):
        score_text = f'Score: {self.score}'
        score_surface = self.settings.get_font(size=25).render(score_text, True, (255, 255, 255))
        score_x = int(self.settings.screen_width - 2 * self.settings.cell_size)
        score_y = int(self.settings.screen_width - 0.5 * self.settings.cell_size)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        self.screen.blit(score_surface, score_rect)

    def _draw_border(self):
        self.border_height_right.draw(self.screen)
        self.border_height_left.draw(self.screen)
        self.border_width_up.draw(self.screen)
        self.border_width_down.draw(self.screen)

    def check_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == self.screen_update:
                self._update()
            if event.type == pygame.KEYDOWN:
                self._change_direction(event=event)
                self._update()

    def _game_over_screen(self):
        pygame.time.delay(self.settings.screen_delay_on_game_over)
        saving_score_modal = SavingScoreModal(settings=self.settings, score=self.score)
        saving_score_modal.draw_score_input_modal(screen=self.screen)

    def play_game(self):
        clock = pygame.time.Clock()
        pygame.time.set_timer(self.screen_update, self.settings.screen_update_time)
        while True:
            self.check_for_events()
            if self.game_over:
                self._game_over_screen()
                break
            else:
                self.darkness.update_snake_position(self.snake.snake_body.position)
                self._draw_elements()
            pygame.display.update()
            clock.tick(self.settings.fps)
