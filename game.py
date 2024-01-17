GRAVITATION = 100
STANDARD_JUMP_SPEED = 4
SCREEN_SIZE = (500, 1000)
STOP_FLOATING_POINT = 0.4  # Определяет, при каком значении скорости Санс сразу полетит вниз
MAX_HOR_SPEED = 3
DYNAMIC_POINT_LIMIT = 100  # Через сколько очков будет спарвнится платформа
SPIKE_SPAWN_PROBABILITY = 10
BOMB_SPAWN_PROBABILITY = 15
BOMB_TIMER_LIMIT = 10


from random import randrange
import pygame
from game_objects import Sas, KillingSas, Bomb, PLATFORM_WIDTH, SPIKE_WIDTH, BOMB_WIDTH, load_image
from caratel import Sans, WIDTH, HEIGHT
from cursor import Cursor


def set_difficulty(level):
    global SPIKE_SPAWN_PROBABILITY, BOMB_SPAWN_PROBABILITY
    if level == 1:
        SPIKE_SPAWN_PROBABILITY = 15
        BOMB_SPAWN_PROBABILITY = 20
    elif level == 2:
        SPIKE_SPAWN_PROBABILITY = 6
        BOMB_SPAWN_PROBABILITY = 10
    else:
        SPIKE_SPAWN_PROBABILITY = 3
        BOMB_SPAWN_PROBABILITY = 5


def create_starfield(platforms_group):
    for y in range(10, height, DYNAMIC_POINT_LIMIT):
        x = randrange(width - PLATFORM_WIDTH)
        platform = Sas(x, y, platforms_group)


def spawn_platform(platforms_group):
    x = randrange(width - PLATFORM_WIDTH)
    platform = Sas(x, 0, platforms_group)
    if randrange(SPIKE_SPAWN_PROBABILITY) == 0:
        x1 = randrange(width - SPIKE_WIDTH)
        spike = KillingSas(x1, -100, spike_group)
    if randrange(BOMB_SPAWN_PROBABILITY) == 0:
        x2 = randrange(width - BOMB_WIDTH)
        bomb = Bomb(x2, 0, bomb_group)
        bombs_on_screen.append(bomb)


def buttons_interaction(character):
    """Обработка кнопочных событий"""

    # Relative control

    cursor_position_relatively_to_center = pygame.mouse.get_pos()[0] - width / 2
    character.hor_velocity = cursor_position_relatively_to_center / (width / 2) * MAX_HOR_SPEED

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
                cursor_sprite.rect.x, cursor_sprite.rect.y = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for index, bomb in enumerate(zip(bombs_on_screen, bomb_group)):
                if pygame.sprite.spritecollideany(bomb[1], cursor_group):
                    bomb[1].kill()
                    bombs_on_screen.remove(bomb[0])

    return running_flag


def move(character, character_sprite, platforms_group):
    """Двигает спрайты"""
    global points, dynamic_points

    character.change_character_sprite()

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
        for bomb in bomb_group:
            bomb.rect = bomb.rect.move((0, -character.vert_velocity))


def bomb_detonation():
    for bomb in zip(bombs_on_screen, bomb_group):
        bomb[0].timer += tick / 1000
        if bomb[0].timer > BOMB_TIMER_LIMIT and sans_group.sprites():
            sans_group.sprites()[0].kill()


def killing_sprites():  # Killing sprites that are offscreeen
    for platform in platform_group:
        if platform.rect.y > height - 50:
            platform.kill()
    for spike in spike_group:
        if spike.rect.y > height - 50:
            spike.kill()
    for index, bomb in enumerate(zip(bombs_on_screen, bomb_group)):
        if bomb[1].rect.y > height - 50:
            bomb[1].kill()
            bombs_on_screen.remove(bomb[0])


def render():
    screen.fill((255, 255, 255))
    platform_group.draw(screen)
    sans_group.draw(screen)
    cursor_group.draw(screen)
    spike_group.draw(screen)
    bomb_group.draw(screen)
    for bomb in bombs_on_screen:
        bomb.draw_timer(int(BOMB_TIMER_LIMIT - bomb.timer), screen, bomb.sprite.rect[0], bomb.sprite.rect[1])
    pygame.display.flip()


points = 0  # Счёт игрока
dynamic_points = 0  # То же самое, что points, но обнуляется каждые DYNAMIC_POINTS_LIMIT очков, создавая платформу
if __name__ == '__main__':
    # Pygame and screen initialization
    pygame.init()
    pygame.display.set_caption('Doodle Moodle')
    size = width, height = SCREEN_SIZE
    screen = pygame.display.set_mode(size)
    running = True

    # Sprite groups, start screen and character initialization
    platform_group = pygame.sprite.Group()
    sans_group = pygame.sprite.Group()
    cursor_group = pygame.sprite.Group()
    spike_group = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()
    timer_group = pygame.sprite.Group
    create_starfield(platform_group)

    # Milcanceuos (Как это слово пишется?) init
    bombs_on_screen = []
    oleg = Sans((width / 2, height / 2), sans_group)  # Олег Санс

    pygame.mouse.set_pos((width + oleg.width) / 2, (height + oleg.height) / 2)
    cursor = Cursor(*map(lambda x: x / 2, SCREEN_SIZE), cursor_group)
    pygame.mouse.set_visible(False)

    # Clock init
    clock = pygame.time.Clock()
    while running:
        tick = clock.tick(200)
        # Events reading
        running = buttons_interaction(oleg)

        # Character movement
        for sans in sans_group:
            move(oleg, sans, platform_group)

        bomb_detonation()

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
        oleg.vert_velocity += 0.02 * GRAVITATION / 100
        if abs(oleg.vert_velocity) < STOP_FLOATING_POINT:  # Определяет, при каком значении скорости Санс сразу полетит вниз
            oleg.vert_velocity = 1

        killing_sprites()
        render()

pygame.quit()
