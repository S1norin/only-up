WIDTH, HEIGHT = 40, 10

import os
import sys
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('assets', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Sas:

    def __init__(self, x, y, spice_group):
        self.x, self.y = x, y
        original_image = load_image("platform.png")
        transfromed_image = pygame.transform.scale(original_image, (WIDTH, HEIGHT))
        sprite = pygame.sprite.Sprite(spice_group)
        sprite.image = transfromed_image
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = self.x, self.y