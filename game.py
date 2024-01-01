SANS_POSTITION = (200, 300)

from random import randrange
import pygame
from platform import Sas
from caratel import Sans

from time import sleep


def create_starfield():
    for y in range(10, 590, 80):
        x = randrange(400)
        central_platform = Sas(x, y, all_spice) # RIP oleg, oleg1, oleg2. Теперь олегом называется только главный персонаж
        left_platform = Sas(x + 80, y, all_spice)
        right_platform = Sas(x - 80, y, all_spice)


speed = 60
if __name__ == '__main__':
    # Pygame and screen initialization
    pygame.init()
    pygame.display.set_caption('Doodle Moodle')
    size = width, height = 400, 600
    screen = pygame.display.set_mode(size)
    running = True

    # Sprite group, start screen and character initialization
    all_spice = pygame.sprite.Group()
    sans_group = pygame.sprite.Group()
    create_starfield()
    oleg = Sans(SANS_POSTITION, sans_group)  # Олег Санс
    pygame.mouse.set_pos((SANS_POSTITION[0] + (oleg.width) / 2,
                          SANS_POSTITION[1] + (oleg.height) / 2))  # Центруем мышь. Почему-то работает через раз
    pygame.mouse.set_visible(True)

    # Time and physics
    movement = 0
    clock = pygame.time.Clock()
    while running:

        for event in pygame.event.get(): # Exit check
            if event.type == pygame.QUIT:
                running = False
        if event.type == pygame.MOUSEMOTION: # moving character with mouse
            for sans in sans_group:
                sans.rect.x = pygame.mouse.get_pos()[0] - (oleg.width) / 2

        if pygame.sprite.spritecollideany(sans_group.sprites()[0], all_spice):
            sans_inside = True

        for sprite in all_spice: # Killing sprites that are offscreeen
            if sprite.rect.y > 550:
                sprite.kill()
            sprite.rect = sprite.rect.move(0, 1)

        clock.tick(speed) # ???
        speed += 1

        # Render
        screen.fill((0, 0, 0))
        all_spice.draw(screen)
        sans_group.draw(screen)
        pygame.display.flip()
pygame.quit()
