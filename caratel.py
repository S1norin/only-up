from platform import load_image
import pygame
WIDTH, HEIGHT = 25, 40
GRAVITATION = 1



class Sans:
    def __init__(self, x, y, spice_group):
        self.x, self.y = x, y
        original_image = load_image("character.png")
        transfromed_image = pygame.transform.scale(original_image, (WIDTH, HEIGHT))
        self.sprite = pygame.sprite.Sprite(spice_group)
        self.sprite.image = transfromed_image
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x, self.sprite.rect.y = self.x, self.y
        self.x = 100
        self.y = 100
        self.vert_velocity = 0
        self.hor_velocity = 0
        self.acceleration = GRAVITATION

    def collision(self):
        pass

    def death(self):
        pass