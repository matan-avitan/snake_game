from pygame import Surface, image

from utils.utils import resource_path


class SpriteExtractor:

    def __init__(self, path: str):
        self.sprite = image.load(resource_path(path)).convert_alpha()

    def get_sprite(self, x: int, y: int, width: int, height: int) -> Surface:
        sprite = Surface([width, height])
        sprite.blit(self.sprite, (0, 0), (x, y, width, height))
        sprite.set_colorkey((0, 0, 0))
        return sprite
