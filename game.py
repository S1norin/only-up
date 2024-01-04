GRAVITATION = 3
STANDARD_JUMP_SPEED = 4
SCREEN_SIZE = (500, 1000)
STOP_FLOATING_POINT = 0.4
from random import randrange
import pygame
from platform import Sas
from caratel import Sans
from cursor import Cursor

from time import sleep


def spawn_platform(platforms_group):
    x = randrange(width)
    platform = Sas(x, 0, platforms_group)


def create_starfield(platforms_group):
    for y in range(10, height, 100):
        x = randrange(width)
        platform = Sas(x, y, platforms_group)


def buttons_interaction(character):
    """Обработка кнопочных событий"""

    # Relative control

    cursor_position_relatively_to_center = pygame.mouse.get_pos()[0] - width / 2
    character.hor_velocity = cursor_position_relatively_to_center / 100

    running_flag = True
    for event in pygame.event.get():  # Exit check
        if event.type == pygame.QUIT:
            running_flag = False
        elif event.type == pygame.MOUSEMOTION:
            for cursor_sprite in cursor_group:
                if pygame.mouse.get_pos()[0] < SCREEN_SIZE[0] / 2:
                    cursor.flip(False)
                else:
                    cursor.flip(True)
                cursor_sprite.rect = pygame.mouse.get_pos()


    return running_flag


def move(character, character_sprite, platforms_group):
    """Двигает спрайты"""
    global points, dynamic_points

    if character_sprite.rect.y + character.vert_velocity > 250:
        character_sprite.rect = character_sprite.rect.move((round(character.hor_velocity), character.vert_velocity))
    else:
        character_sprite.rect = character_sprite.rect.move((round(character.hor_velocity), 0))
        points -= character.vert_velocity
        dynamic_points -= character.vert_velocity
        if dynamic_points > 100:
            spawn_platform(platforms_group)
            dynamic_points = 0
        for platform in platforms_group:
            platform.rect = platform.rect.move((0, -character.vert_velocity))


speed = 60
points = 0  # Счёт игрока
dynamic_points = 0  # То же самое, что points, но обнуляется каждые 100 очков, создавая платформу
if __name__ == '__main__':
    # Pygame and screen initialization
    pygame.init()
    pygame.display.set_caption('Doodle Moodle')
    size = width, height = SCREEN_SIZE
    screen = pygame.display.set_mode(size)
    running = True

    # Sprite group, start screen and character initialization
    all_spice = pygame.sprite.Group()
    sans_group = pygame.sprite.Group()
    cursor_group = pygame.sprite.Group()
    create_starfield(all_spice)

    oleg = Sans((width / 2, height / 2), sans_group)  # Олег Санс
    pygame.mouse.set_pos(((SCREEN_SIZE[0] + oleg.width) / 2,
                          (SCREEN_SIZE[1] + oleg.height) / 2))

    cursor = Cursor(*map(lambda x: x/2, SCREEN_SIZE), cursor_group)
    pygame.mouse.set_visible(False)

    # Clock init
    clock = pygame.time.Clock()

    hor_acceleration = 0
    while running:
        tick = clock.tick(120) # Вывел тик в переменную в начале цикла, чтобы при множественном обращении не ломать вообще всё, что завязано на времени
        # Events reading
        running = buttons_interaction(oleg)

        # Character movement
        for sans in sans_group:
            move(oleg, sans, all_spice)

        # Collision
        if oleg.vert_velocity >= 0:
            if pygame.sprite.spritecollideany(sans_group.sprites()[0], all_spice):
                oleg.collision(STANDARD_JUMP_SPEED)

        # Gravitation
        oleg.vert_velocity += ((GRAVITATION * tick) / 1000)
        if abs(oleg.vert_velocity) < STOP_FLOATING_POINT: # Определяет, при каком значении скорости Санс сразу полетит вниз
            oleg.vert_velocity = 1

        for sprite in all_spice:  # Killing sprites that are offscreeen
            if sprite.rect.y > height - 50:
                sprite.kill()

        # Render
        screen.fill((255, 255, 255))
        all_spice.draw(screen)
        sans_group.draw(screen)
        cursor_group.draw(screen)
        pygame.display.flip()
pygame.quit()
