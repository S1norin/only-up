SPIKES_WIDTH, SPIKES_HEIGHT = 25, 100

import pygame
from platform import load_image

class KillingSas():
    def __init__(self, x, y, spice_group):
        self.x, self.y = x, y
        self.width, self.height = SPIKES_WIDTH, SPIKES_HEIGHT
        original_image = load_image("spikes.png")
        transfromed_image = pygame.transform.scale(original_image, (SPIKES_WIDTH, SPIKES_HEIGHT))
        sprite = pygame.sprite.Sprite(spice_group)
        sprite.image = transfromed_image
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = self.x, self.y
