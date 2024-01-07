PLATFORM_WIDTH, PLATFROM_HEIGHT = 40, 10
SPIKE_WIDTH, SPIKE_HEIGHT = 25, 100
BOMB_WIDTH, BOMB_HEIGHT = 40, 40

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


class Sprite:
    def __init__(self, x, y, spice_group):
        self.x, self.y = x, y
        self.set_size()
        original_image = self.orig_image()
        transformed_image = pygame.transform.scale(original_image, (self.width, self.height))
        sprite = pygame.sprite.Sprite(spice_group)
        sprite.image = transformed_image
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = self.x, self.y

    def orig_image(self):
        raise FileNotFoundError("Image not selected")

    def set_size(self):
        self.width, self.height = None, None


class Sas(Sprite):
    def orig_image(self):
        return load_image("platform.png")

    def set_size(self):
        self.width, self.height = PLATFORM_WIDTH, PLATFROM_HEIGHT


class KillingSas(Sprite):
    def orig_image(self):
        return load_image("spikes.png")

    def set_size(self):
        self.width, self.height = SPIKE_WIDTH, SPIKE_HEIGHT

class Bomb(Sprite):
    def __init__(self, x, y, spice_group):
        super().__init__(x, y, spice_group)
        self.timer = 0

    def orig_image(self):
        return load_image("bomb.png")

    def set_size(self):
        self.width, self.height = BOMB_WIDTH, BOMB_HEIGHT
