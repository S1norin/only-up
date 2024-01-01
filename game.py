SANS_POSTITION = (200, 300)
GRAVITATION = 3
STANDARD_JUMP_SPEED = 7
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
    pygame.mouse.set_visible(False)

    # Time and physics
    clock = pygame.time.Clock()
    clock.tick(60)
    while running:
        for event in pygame.event.get(): # Exit check
            if event.type == pygame.QUIT:
                running = False

            # Interaction with main character
            for sans in sans_group:
                if event.type == pygame.MOUSEMOTION:  # moving character with mouse
                    sans.rect.x = pygame.mouse.get_pos()[0] - (oleg.width) / 2
        for sans in sans_group:
            sans.rect = sans.rect.move((0, oleg.vert_velocity))

        if oleg.vert_velocity >= 0:
            # Колизия засчтиывается, даже если ты ты сталкиваешься с блоком лбом. Нужно уменьшать хитбокс
            if pygame.sprite.spritecollideany(sans_group.sprites()[0], all_spice):
                oleg.collision(STANDARD_JUMP_SPEED)
        oleg.vert_velocity += (GRAVITATION * clock.tick(60)) / 750

        for sprite in all_spice: # Killing sprites that are offscreeen
            if sprite.rect.y > 550:
                sprite.kill()

        # Render
        screen.fill((0, 0, 0))
        all_spice.draw(screen)
        sans_group.draw(screen)
        pygame.display.flip()
pygame.quit()
