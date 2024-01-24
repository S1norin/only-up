from game_objects import load_image
import pygame
WIDTH, HEIGHT = 50, 80
GRAVITATION = 1


class Hitbox:
    def __init__(self, position, spice_group, size=(WIDTH, HEIGHT)):
        # Setting up coords and size
        self.x, self.y = position[0], position[1]
        self.width, self.height = size
        # Initializing sprite
        original_image = load_image("void.png")
        transfromed_image = pygame.transform.scale(original_image, size)
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


class Sans(Hitbox):
    def change_character_sprite(self):
        if self.hor_velocity < -1:
            img_name = "Cat_left_final.png"
        elif self.hor_velocity < 0:
            img_name = "Cat_lean_left_final.png"
        elif self.hor_velocity < 1:
            img_name = "Cat_lean_right_final.png"
        else:
            img_name = "Cat_right_final.png"
        original_image = load_image(img_name)
        transfromed_image = pygame.transform.scale(original_image, (WIDTH, HEIGHT))
        self.sprite.image = transfromed_image
