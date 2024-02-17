import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, image=None, pos=(0, 0), text_input="", font=None, base_color=(255, 255, 255),
                 hovering_color=(200, 200, 200), value=None):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(center=pos) if self.image else pygame.Rect(pos[0], pos[1], 0, 0)
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.value = value if value is not None else self.text_input
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
