from game_objects import load_image
import pygame
WIDTH, HEIGHT = 25, 40
GRAVITATION = 1



class Sans:
    def __init__(self, position, spice_group):
        # Setting up coords and size
        self.x, self.y = position[0], position[1]
        self.width, self.height = WIDTH, HEIGHT
        # Initializing sprite
        original_image = load_image("character.png")
        transfromed_image = pygame.transform.scale(original_image, (WIDTH, HEIGHT))
        self.sprite = pygame.sprite.Sprite(spice_group)
        self.sprite.image = transfromed_image
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x, self.sprite.rect.y = self.x, self.y
        # Speeds
        self.vert_velocity = 0
        self.hor_velocity = 0
        self.acceleration = GRAVITATION

    def collision(self, velocity):
        self.vert_velocity = -velocity

    def death(self):
        pass