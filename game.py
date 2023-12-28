from random import randrange
import pygame
from platform import Sas
from caratel import Sans

from time import sleep

def create_starfield():
    for y in range(10, 590, 80):
        x = randrange(400)
        oleg = Sas(x, y, all_spice)
        oleg1 = Sas(x + 80, y, all_spice)
        oleg2 = Sas(x - 80, y, all_spice)
        oleg3 = Sans(200, 300, sans_group) # Андей Санс


speed = 60
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Doodle Moodle')
    size = width, height = 400, 600
    screen = pygame.display.set_mode(size)
    running = True
    all_spice = pygame.sprite.Group()
    sans_group = pygame.sprite.Group()
    clock = pygame.time.Clock()
    create_starfield()
    movement = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for sans in sans_group:
                    movement += 1
                    if movement == 10:
                        sans.rect = sans.rect.move(-1, 0)
                        movement = 0
            else:
                for sans in sans_group:
                    movement += 1
                    if movement == 10:
                        sans.rect = sans.rect.move(1, 0)
                        movement = 0

        if pygame.sprite.spritecollideany(sans_group.sprites()[0], all_spice):
            sans_inside = True

        clock.tick(speed)
        speed += 1
        for sprite in all_spice:
            if sprite.rect.y > 550:
                sprite.kill()
            sprite.rect = sprite.rect.move(0, 1)
        screen.fill((0, 0, 0))
        all_spice.draw(screen)
        sans_group.draw(screen)
        pygame.display.flip()
pygame.quit()
