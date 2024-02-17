import sys
from typing import List, Optional

import pygame
from pygame import Surface
from elements import Button
from game_settings import Settings
from screens.base_screen import BaseScreen
from screens.options.objects import ButtonOptions, ButtonOption


class Options(BaseScreen):

    def __init__(self, settings: Optional[Settings], screen: Optional[Surface]):
        super().__init__(settings=settings, screen=screen)
        self.button_options = ButtonOptions()
        self.back = False
        self.selected_snake_color = self.settings.snake_color
        self.selected_board_type = self.settings.tile_type
        self.selected_difficult = self.settings.difficulty
        self.selected_darkness_mode = self.settings.darkness_mode
        self._get_all_buttons()

    def _get_all_buttons(self):
        self.color_buttons = self._get_buttons(button_option_type=self.button_options.color_buttons,
                                               selected_option=self.selected_snake_color, y_position=2,
                                               starting_x_position=4)

        self.board_types_buttons = self._get_buttons(button_option_type=self.button_options.board_types,
                                                     selected_option=self.selected_board_type, y_position=4,
                                                     starting_x_position=4)

        self.difficult_types_buttons = self._get_buttons(button_option_type=self.button_options.difficult_types,
                                                         selected_option=self.selected_difficult, y_position=6,
                                                         starting_x_position=4)

        self.darkness_buttons = self._get_buttons(button_option_type=self.button_options.darkness_mode_options,
                                                  selected_option=self.selected_darkness_mode, y_position=8,
                                                  starting_x_position=5)
        self.options_back = self._get_button(text="Back", y_position=5.5)

    def _draw_options_title(self, text: str, screen_position: int):
        options_text = self.settings.get_font(50).render(text, True, "black")
        options_rect = options_text.get_rect(
            center=(self.settings.screen_width // 2, self.settings.screen_height // 12 * screen_position))
        self.screen.blit(options_text, options_rect)

    def _get_buttons(self, button_option_type: List[ButtonOption], selected_option, y_position: int,
                     starting_x_position: int) -> List[Button]:
        buttons = []
        for index, board_types in enumerate(button_option_type):
            is_selected = board_types.value == selected_option
            x_position = self.settings.screen_width // 12 * (2 * index + starting_x_position)
            color = board_types.color if is_selected else "black"
            button = Button(
                image=None,
                pos=(x_position, self.settings.screen_height // 12 * y_position),
                text_input=board_types.text,
                font=self.settings.get_font(40),
                base_color=color,
                hovering_color="white",
                value=board_types.value
            )
            buttons.append(button)
        return buttons

    def _draw_button_type(self, buttons_type: List[Button]):
        for button in buttons_type:
            button.update_text()
            button.update(self.screen)

    def draw_buttons(self):
        self._get_all_buttons()
        self._draw_button_type(buttons_type=self.color_buttons)
        self._draw_button_type(buttons_type=self.board_types_buttons)
        self._draw_button_type(buttons_type=self.difficult_types_buttons)
        self._draw_button_type(buttons_type=self.darkness_buttons)
        self.options_back.update_text()
        self.options_back.update(self.screen)

    def _draw_titles(self):
        self._draw_options_title(text='Select Snake Color:', screen_position=1)
        self._draw_options_title(text='Select Board Type:', screen_position=3)
        self._draw_options_title(text='Select Difficult Type:', screen_position=5)
        self._draw_options_title(text='Darkness Mode:', screen_position=7)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if self.options_back.check_for_input(self.mouse_position):
                    self.back = True
                for color_button in self.color_buttons:
                    if event.type == pygame.MOUSEBUTTONUP and color_button.check_for_input(self.mouse_position):
                        self.selected_snake_color = color_button.value
                        self.settings.snake_color = color_button.value
                for board_types_button in self.board_types_buttons:
                    if event.type == pygame.MOUSEBUTTONUP and board_types_button.check_for_input(
                            self.mouse_position):
                        self.selected_board_type = board_types_button.value
                        self.settings.tile_type = board_types_button.value
                for difficult_types_button in self.difficult_types_buttons:
                    if event.type == pygame.MOUSEBUTTONUP and difficult_types_button.check_for_input(
                            self.mouse_position):
                        self.selected_difficult = difficult_types_button.value
                        self.settings.update_difficulty(difficult_types_button.value)
                for darkness_button in self.darkness_buttons:
                    if event.type == pygame.MOUSEBUTTONUP and darkness_button.check_for_input(
                            self.mouse_position):
                        self.selected_darkness_mode = darkness_button.value
                        self.settings.update_darkness_mode(darkness_button.value)

    def options(self):
        while True:
            self.update_mouse_position()
            self.draw_default_background()
            self._draw_titles()
            self.draw_buttons()
            self.check_events()
            if self.back:
                break
            pygame.display.update()
