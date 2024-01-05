GRAVITATION = 3
STANDARD_JUMP_SPEED = 4
SCREEN_SIZE = (500, 1000)
STOP_FLOATING_POINT = 0.4  # Определяет, при каком значении скорости Санс сразу полетит вниз
MAX_HOR_SPEED = 7
DYNAMIC_POINT_LIMIT = 100  # Через сколько очков будет спарвнится платформа
SPIKE_SPAWN_PROPABILITY = 10
from random import randrange
import pygame
from platform import Sas, PLATFORM_WIDTH
from spikes import KillingSas, SPIKES_WIDTH
from caratel import Sans
from cursor import Cursor


def spawn_platform(platforms_group):
    x = randrange(width - SPIKES_WIDTH)
    platform = Sas(x, 0, platforms_group)
    if randrange(SPIKE_SPAWN_PROPABILITY) == 0:
        x1 = randrange(width - SPIKES_WIDTH)
        spike = KillingSas(x1, -100, spike_group)


def create_starfield(platforms_group):
    for y in range(10, height, DYNAMIC_POINT_LIMIT):
        x = randrange(width - PLATFORM_WIDTH)
        platform = Sas(x, y, platforms_group)


def buttons_interaction(character):
    """Обработка кнопочных событий"""

    # Relative control

    cursor_position_relatively_to_center = pygame.mouse.get_pos()[0] - width / 2
    character.hor_velocity = cursor_position_relatively_to_center / (width / 2) * MAX_HOR_SPEED
    if abs(character.hor_velocity) < MAX_HOR_SPEED * 0.3:
        if character.hor_velocity > 0:
            character.hor_velocity = MAX_HOR_SPEED * 0.25
        else:
            character.hor_velocity = -MAX_HOR_SPEED * 0.25

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

    if character_sprite.rect.x < 0:
        character_sprite.rect.x = width - character.width
    elif character.sprite.rect.x > width + character.width:
        character_sprite.rect.x = 0
    if character_sprite.rect.y + character.vert_velocity > 250:
        character_sprite.rect = character_sprite.rect.move((round(character.hor_velocity), character.vert_velocity))
    else:
        character_sprite.rect = character_sprite.rect.move((round(character.hor_velocity), 0))

        points -= character.vert_velocity
        dynamic_points -= character.vert_velocity
        if dynamic_points > DYNAMIC_POINT_LIMIT:
            spawn_platform(platforms_group)
            dynamic_points = 0
        for platform in platforms_group:
            platform.rect = platform.rect.move((0, -character.vert_velocity))
        for spike in spike_group:
            spike.rect = spike.rect.move((0, -character.vert_velocity))


speed = 60
points = 0  # Счёт игрока
dynamic_points = 0  # То же самое, что points, но обнуляется каждые DYNAMIC_POINTS_LIMIT очков, создавая платформу
if __name__ == '__main__':
    # Pygame and screen initialization
    pygame.init()
    pygame.display.set_caption('Doodle Moodle')
    size = width, height = SCREEN_SIZE
    screen = pygame.display.set_mode(size)
    running = True

    # Sprite group, start screen and character initialization
    platform_group = pygame.sprite.Group()
    sans_group = pygame.sprite.Group()
    cursor_group = pygame.sprite.Group()
    spike_group = pygame.sprite.Group()
    create_starfield(platform_group)

    oleg = Sans((width / 2, height / 2), sans_group)  # Олег Санс
    pygame.mouse.set_pos(((SCREEN_SIZE[0] + oleg.width) / 2,
                          (SCREEN_SIZE[1] + oleg.height) / 2))

    cursor = Cursor(*map(lambda x: x / 2, SCREEN_SIZE), cursor_group)
    pygame.mouse.set_visible(False)

    # Clock init
    clock = pygame.time.Clock()

    hor_acceleration = 0
    while running:
        tick = clock.tick(120)
        # Events reading
        running = buttons_interaction(oleg)

        # Character movement
        for sans in sans_group:
            move(oleg, sans, platform_group)

        # Collision
        try:
            if oleg.vert_velocity >= 0:
                if pygame.sprite.spritecollideany(sans_group.sprites()[0], platform_group):
                    oleg.collision(STANDARD_JUMP_SPEED)
            if pygame.sprite.spritecollideany(sans_group.sprites()[0], spike_group):
                sans_group.sprites()[0].kill()
            for spike in spike_group:
                while pygame.sprite.spritecollideany(spike, platform_group):
                    pygame.sprite.spritecollideany(spike, platform_group).kill()
                    spawn_platform(platform_group)
        except IndexError:
            pass

        # Gravitation
        oleg.vert_velocity += ((GRAVITATION * tick) / 1000)
        if abs(oleg.vert_velocity) < STOP_FLOATING_POINT:  # Определяет, при каком значении скорости Санс сразу полетит вниз
            oleg.vert_velocity = 1

        for platform in platform_group:  # Killing sprites that are offscreeen
            if platform.rect.y > height - 50:
                platform.kill()
        for spike in spike_group:
            if spike.rect.y > height - 50:
                spike.kill()

        # Render
        screen.fill((255, 255, 255))
        platform_group.draw(screen)
        sans_group.draw(screen)
        cursor_group.draw(screen)
        spike_group.draw(screen)
        pygame.display.flip()
pygame.quit()
