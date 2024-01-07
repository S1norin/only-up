CURSOR_WIDTH, CURSOR_HEIGHT = 30, 20
import pygame
from game_objects import load_image

class Cursor:
    def __init__(self, x, y, spice_group):
        self.orientation = True
        self.x, self.y = x, y
        original_image = load_image("cursor.png")
        self.transformed_image = pygame.transform.scale(original_image, (CURSOR_WIDTH, CURSOR_HEIGHT))
        self.sprite = pygame.sprite.Sprite(spice_group)
        self.sprite.image = self.transformed_image
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x, self.sprite.rect.y = self.x, self.y

    def flip(self, orientation):
        if self.orientation == orientation:
            return None
        else:
            self.sprite.image = pygame.transform.flip(self.sprite.image, True, False)
            self.orientation = orientation


