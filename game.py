GRAVITATION = 4
STANDARD_JUMP_SPEED = 4
SCREEN_SIZE = (1000, 1000)
MAX_HOR_SPEED = 3
from random import randrange
import pygame
from platform import Sas
from caratel import Sans

from time import sleep


def create_starfield():
    for y in range(10, height, 100):
        x = randrange(width)
        central_platform = Sas(x, y, all_spice) # RIP oleg, oleg1, oleg2. Теперь олегом называется только главный персонаж
        left_platform = Sas(x + 80, y, all_spice)
        right_platform = Sas(x - 80, y, all_spice)


speed = 60
if __name__ == '__main__':
    # Pygame and screen initialization
    pygame.init()
    pygame.display.set_caption('Doodle Moodle')
    size = width, height = SCREEN_SIZE
    screen = pygame.display.set_mode(size)
    running = True

    # Sprite group, start screen and character initialization
    center_of_screen = (width / 2, height / 2)
    all_spice = pygame.sprite.Group()
    sans_group = pygame.sprite.Group()
    create_starfield()
    oleg = Sans(center_of_screen, sans_group)  # Олег Санс
    pygame.mouse.set_pos((center_of_screen[0] + (oleg.width) / 2,
                          center_of_screen[1] + (oleg.height) / 2))  # Центруем мышь. Почему-то работает через раз
    pygame.mouse.set_visible(True)

    # Time and physics
    clock = pygame.time.Clock()

    hor_acceleration = 0
    while running:
        for event in pygame.event.get(): # Exit check
            if event.type == pygame.QUIT:
                running = False

            # Interaction with main character
            for sans in sans_group:
                if event.type == pygame.KEYDOWN:  # moving character with arrow buttons
                    if pygame.key.get_pressed()[pygame.K_LEFT]:
                        hor_acceleration = -0.05
                    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                        hor_acceleration = 0.05
                elif event.type == pygame.KEYUP:
                    hor_acceleration = 0

        if abs(oleg.hor_velocity + hor_acceleration) <= MAX_HOR_SPEED:
            oleg.hor_velocity += hor_acceleration

        # Gravitation and inertion
        for sans in sans_group:
            sans.rect = sans.rect.move((round(oleg.hor_velocity), oleg.vert_velocity))

        if oleg.vert_velocity >= 0:
            # Колизия засчтиывается, даже если ты ты сталкиваешься с блоком лбом. Нужно уменьшать хитбокс, чтобы он был только в ногах
            if pygame.sprite.spritecollideany(sans_group.sprites()[0], all_spice):
                oleg.collision(STANDARD_JUMP_SPEED)
        oleg.vert_velocity += ((GRAVITATION * clock.tick(120)) / 750)

        for sprite in all_spice: # Killing sprites that are offscreeen
            if sprite.rect.y > height - 50:
                sprite.kill()

        # Render
        screen.fill((0, 0, 0))
        all_spice.draw(screen)
        sans_group.draw(screen)
        pygame.display.flip()
pygame.quit()
