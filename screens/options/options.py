import sys
import pygame
from pygame import Surface
from elements import Button
from game_settings import Settings


class Options:
    COLOR_BUTTONS = [
        {"text": "Red", "color": "red", 'value': 'red'},
        {"text": "Brown", "color": "brown", 'value': 'brown'},
        {"text": "Green", "color": "green", 'value': 'green'},
    ]
    BOARD_TYPE = [
        {"text": "Grass", "color": "green", 'value': 'grass'},
        {"text": "Stone", "color": "gray", 'value': 'stone'},
        {"text": "Sand", "color": "brown", 'value': 'dirt'},
    ]
    DIFFICULT_TYPE = [
        {"text": "Easy", "color": "green", 'value': 'easy'},
        {"text": "Medium", "color": "orange", 'value': 'medium'},
        {"text": "Hard", "color": "red", 'value': 'hard'},
    ]
    MENU_COVER_PATH = 'assets/snake-game-cover.jpg'

    def __init__(self, settings: Settings, screen: Surface):
        self.screen = screen
        self.settings = settings
        self.back = False
        self.selected_snake_color = self.settings.snake_color
        self.selected_board_type = self.settings.tile_type
        self.selected_difficult = self.settings.difficulty
        self.game_cover = pygame.transform.scale(surface=pygame.image.load(self.MENU_COVER_PATH),
                                                 size=self.settings.screen_dimensions)

    def _get_font(self, size):
        return pygame.font.SysFont(self.settings.font, size=size)

    def _get_button(self, text, y_position, x_position=None, is_selected=False, value=None) -> Button:
        color = "blue" if is_selected else "black"
        x_position = self.settings.screen_width // 2 if not x_position else x_position
        return Button(image=None,
                      pos=(x_position, self.settings.screen_height // 9 * y_position),
                      text_input=text,
                      font=self._get_font(50),
                      base_color=color,
                      hovering_color="white",
                      value=value
                      )

    def _draw_snake_color_options_title(self):
        options_text = self._get_font(50).render("Select Snake Color:", True, "black")  # Adjusted font size
        options_rect = options_text.get_rect(
            center=(self.settings.screen_width // 2, self.settings.screen_height // 9 * 1))
        self.screen.blit(options_text, options_rect)

    def _draw_snake_colors_buttons(self):
        color_buttons = []
        for index, color_button in enumerate(self.COLOR_BUTTONS):
            is_selected = color_button["color"] == self.selected_snake_color
            x_position = self.settings.screen_width // 12 * (2 * index + 4)
            color = color_button["color"] if is_selected else "black"
            button = Button(
                image=None,
                pos=(x_position, self.settings.screen_height // 9 * 2),
                text_input=color_button["text"],
                font=self._get_font(40),
                base_color=color,
                hovering_color="white",
                value=color_button["color"]
            )

            button.update_text()
            button.update(self.screen)
            color_buttons.append(button)
        return color_buttons

    def _draw_board_options_title(self):
        options_text = self._get_font(50).render("Select Board Type:", True, "black")  # Adjusted font size
        options_rect = options_text.get_rect(
            center=(self.settings.screen_width // 2, self.settings.screen_height // 9 * 3))
        self.screen.blit(options_text, options_rect)

    def _draw_board_type_buttons(self):
        board_type_buttons = []
        for index, board_types in enumerate(self.BOARD_TYPE):
            is_selected = board_types["value"] == self.selected_board_type
            x_position = self.settings.screen_width // 12 * (2 * index + 4)
            color = board_types['color'] if is_selected else "black"
            button = Button(
                image=None,
                pos=(x_position, self.settings.screen_height // 9 * 4),
                text_input=board_types["text"],
                font=self._get_font(40),
                base_color=color,
                hovering_color="white",
                value=board_types["value"]
            )

            button.update_text()
            button.update(self.screen)
            board_type_buttons.append(button)
        return board_type_buttons

    def _draw_difficult_options_title(self):
        options_text = self._get_font(50).render("Select Difficult Type:", True, "black")
        options_rect = options_text.get_rect(
            center=(self.settings.screen_width // 2, self.settings.screen_height // 9 * 5))
        self.screen.blit(options_text, options_rect)

    def _draw_difficult_options_buttons(self):
        board_type_buttons = []
        for index, difficult_type in enumerate(self.DIFFICULT_TYPE):
            is_selected = difficult_type["value"] == self.selected_difficult
            x_position = self.settings.screen_width // 12 * (2 * index + 4)
            color = difficult_type['color'] if is_selected else "black"
            button = Button(
                image=None,
                pos=(x_position, self.settings.screen_height // 9 * 6),
                text_input=difficult_type["text"],
                font=self._get_font(40),
                base_color=color,
                hovering_color="white",
                value=difficult_type["value"]
            )

            button.update_text()
            button.update(self.screen)
            board_type_buttons.append(button)
        return board_type_buttons

    def options(self):
        while True:
            options_mouse_pos = pygame.mouse.get_pos()

            # self.screen.fill("#ebedbe")
            self.screen.blit(self.game_cover, (0, 0))

            self._draw_snake_color_options_title()
            color_buttons = self._draw_snake_colors_buttons()

            self._draw_board_options_title()
            board_types_buttons = self._draw_board_type_buttons()

            self._draw_difficult_options_title()
            difficult_types_buttons = self._draw_difficult_options_buttons()

            options_back = self._get_button(text="Back", y_position=8, is_selected=False)
            options_back.update_text()
            options_back.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if options_back.check_for_input(options_mouse_pos):
                        self.back = True
                    for color_button in color_buttons:
                        if event.type == pygame.MOUSEBUTTONUP and color_button.check_for_input(options_mouse_pos):
                            self.selected_snake_color = color_button.value
                            self.settings.snake_color = color_button.value
                    for board_types_button in board_types_buttons:
                        if event.type == pygame.MOUSEBUTTONUP and board_types_button.check_for_input(options_mouse_pos):
                            self.selected_board_type = board_types_button.value
                            self.settings.tile_type = board_types_button.value
                    for difficult_types_button in difficult_types_buttons:
                        if event.type == pygame.MOUSEBUTTONUP and difficult_types_button.check_for_input(
                                options_mouse_pos):
                            self.selected_difficult = difficult_types_button.value
                            self.settings.update_difficulty(difficult_types_button.value)

            if self.back:
                break
            pygame.display.update()
