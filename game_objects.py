PLATFORM_WIDTH, PLATFROM_HEIGHT = 40, 10
SPIKE_WIDTH, SPIKE_HEIGHT = 25, 100
BOMB_WIDTH, BOMB_HEIGHT = 40, 40
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 75
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 1000
import os
import sys
import pygame
import random

all_cat_pictures = [filename for filename in os.listdir("assets") if ".jpg" in filename]
cat_pictures_left = all_cat_pictures[:]

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
        self.sprite = pygame.sprite.Sprite(spice_group)
        self.sprite.image = transformed_image
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x, self.sprite.rect.y = self.x, self.y

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

    def draw_timer(self, time_left, screen, coor_x, coord_y):
        font = pygame.font.Font(None, 30)

        if time_left > 0:
            text = font.render(str(time_left), True, (240, 7, 23))
        else:
            text = font.render("BOOM", True, (240, 7, 23))
        text_x = coor_x + BOMB_WIDTH / 2
        text_y = coord_y + BOMB_HEIGHT
        screen.blit(text, (text_x, text_y))

class Button(Sprite):

    def __init__(self, x, y, spice_group, image_name):
        self.x, self.y = x, y
        self.set_size()
        original_image = self.orig_image(image_name)
        transformed_image = pygame.transform.scale(original_image, (self.width, self.height))
        self.sprite = pygame.sprite.Sprite(spice_group)
        self.sprite.image = transformed_image
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x, self.sprite.rect.y = self.x, self.y

    def orig_image(self, image_name):
        return load_image(image_name)

    def set_size(self):
        self.width, self.height = BUTTON_WIDTH, BUTTON_HEIGHT

class Background(Sprite):

    def orig_image(self):
        global cat_pictures_left
        background = random.choice(cat_pictures_left)
        cat_pictures_left.remove(background)
        if not cat_pictures_left:
            cat_pictures_left = all_cat_pictures[:]
        return load_image(background)

    def set_size(self):
        self.width, self.height = WINDOW_WIDTH, WINDOW_HEIGHT