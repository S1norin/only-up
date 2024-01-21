import random

GRAVITATION = 100
STANDARD_JUMP_SPEED = 4
SCREEN_SIZE = (500, 1000)
STOP_FLOATING_POINT = 0.4  # Определяет, при каком значении скорости Санс сразу полетит вниз
MAX_HOR_SPEED = 3
DYNAMIC_POINT_LIMIT = 100  # Через сколько очков будет спарвнится платформа
BOMB_TIMER_LIMIT = 7

import os
from random import randrange, choice
import pygame
from game_objects import Sas, KillingSas, Bomb, PLATFORM_WIDTH, SPIKE_WIDTH, BOMB_WIDTH, load_image
from caratel import Sans, WIDTH, HEIGHT, Hitbox
from game_objects import Sas, KillingSas, Bomb, Button, Background, PLATFORM_WIDTH, SPIKE_WIDTH, BOMB_WIDTH, \
    BUTTON_WIDTH, \
    BUTTON_HEIGHT
from caratel import Sans
from cursor import Cursor


def set_difficulty(level):
    global SPIKE_SPAWN_PROBABILITY, BOMB_SPAWN_PROBABILITY
    if level == 0:
        SPIKE_SPAWN_PROBABILITY = 15
        BOMB_SPAWN_PROBABILITY = 20
    elif level == 1:
        SPIKE_SPAWN_PROBABILITY = 6
        BOMB_SPAWN_PROBABILITY = 10
    else:
        SPIKE_SPAWN_PROBABILITY = 3
        BOMB_SPAWN_PROBABILITY = 5


def init_interface(buttons_group):
    start_button = Button(width / 2 - BUTTON_WIDTH / 2, height / 2 - height / 6, buttons_group, "Start_button.png")
    if difficulty_clicks % 3 == 0:
        difficulty_buttons = Button(width / 2 - BUTTON_WIDTH / 2, height / 2, buttons_group, "Difficulty_Easy.png")
    elif difficulty_clicks % 3 == 1:
        difficulty_buttons = Button(width / 2 - BUTTON_WIDTH / 2, height / 2, buttons_group, "Difficulty_Advanced.png")
    else:
        difficulty_buttons = Button(width / 2 - BUTTON_WIDTH / 2, height / 2, buttons_group, "Difficulty_Hard.png")


def interface():
    global difficulty_clicks, sans_is_dead
    running_flag = True
    for event in pygame.event.get():  # Exit check
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if width / 2 - BUTTON_WIDTH / 2 < pygame.mouse.get_pos()[
                0] < width / 2 - BUTTON_WIDTH / 2 + BUTTON_WIDTH and height / 2 - height / 6 < pygame.mouse.get_pos()[
                1] < height / 2 - height / 6 + BUTTON_HEIGHT:
                running_flag = False
                sans_is_dead = False
                game_start()
            elif width / 2 - BUTTON_WIDTH / 2 < pygame.mouse.get_pos()[
                0] < width / 2 - BUTTON_WIDTH / 2 + BUTTON_WIDTH and height / 2 < pygame.mouse.get_pos()[
                1] < height / 2 + BUTTON_HEIGHT:
                difficulty_clicks += 1
                for button in buttons_group:
                    button.kill()
    init_interface(buttons_group)
    background_group.draw(screen)
    buttons_group.draw(screen)
    pygame.display.flip()

    return running_flag


def create_starfield(platforms_group):
    for y in range(10, height, DYNAMIC_POINT_LIMIT):
        x = randrange(width - PLATFORM_WIDTH)
        if y == 610:
            platform = Sas(width / 2, y, platforms_group)
        else:
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


def buttons_interaction(character, hitbox):
    """Обработка кнопочных событий"""

    # Relative control

    cursor_position_relatively_to_center = pygame.mouse.get_pos()[0] - width / 2
    character.hor_velocity = cursor_position_relatively_to_center / (width / 2) * MAX_HOR_SPEED
    hitbox.hor_velocity = cursor_position_relatively_to_center / (width / 2) * MAX_HOR_SPEED

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


def move(character, character_sprite, hitbox=False):
    """Двигает спрайты"""
    global points, dynamic_points
    relative_coord = 250
    if hitbox:
        relative_coord = 330
    if character_sprite.rect.x < 0:
        character_sprite.rect.x = width - character.width
    elif character.sprite.rect.x > width + character.width:
        character_sprite.rect.x = 0
    if character_sprite.rect.y + character.vert_velocity > relative_coord:
        character_sprite.rect = character_sprite.rect.move((round(character.hor_velocity), character.vert_velocity))
    else:
        character_sprite.rect = character.sprite.rect.move((round(character.hor_velocity), 0))


def move_platforms(character):
    global points, dynamic_points
    if character.sprite.rect.y + character.vert_velocity <= 250:
        points -= character.vert_velocity
        dynamic_points -= character.vert_velocity
        if dynamic_points > DYNAMIC_POINT_LIMIT:
            spawn_platform(platform_group)
            dynamic_points = 0
        for platform in platform_group:
            platform.rect = platform.rect.move((0, -character.vert_velocity))
        for spike in spike_group:
            spike.rect = spike.rect.move((0, -character.vert_velocity))
        for bomb in bomb_group:
            bomb.rect = bomb.rect.move((0, -character.vert_velocity))


def bomb_detonation():
    for bomb in zip(bombs_on_screen, bomb_group):
        bomb[0].timer += tick / 1000
        if bomb[0].timer > BOMB_TIMER_LIMIT and sans_group.sprites():
            return True
    return False


def killing_sprites():  # Killing sprites that are offscreeen
    global sans_is_dead
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
    for sans in sans_group:
        if sans.rect.y > height:
            sans.kill()
            sans_is_dead = True


def reset_all_objects():
    global platform_group, sans_group, cursor_group, spike_group, bomb_group, timer_group, buttons_group, background_group
    background_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    sans_group = pygame.sprite.Group()
    cursor_group = pygame.sprite.Group()
    spike_group = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()
    timer_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()


def render():
    screen.fill((255, 255, 255))
    background_group.draw(screen)
    platform_group.draw(screen)
    sans_group.draw(screen)
    cursor_group.draw(screen)
    spike_group.draw(screen)
    bomb_group.draw(screen)
    for bomb in bombs_on_screen:
        bomb.draw_timer(int(BOMB_TIMER_LIMIT - bomb.timer), screen, bomb.sprite.rect[0], bomb.sprite.rect[1])
    pygame.display.flip()


def game_start():
    reset_all_objects()
    global bombs_on_screen, cursor, clock, oleg, legs
    # Milcanceuos (Как это слово пишется?) init
    background_sprite = Background(0, 0, background_group)
    set_difficulty(difficulty_clicks % 3)
    oleg = Sans((width / 2, height / 2), sans_group)  # Олег Санс
    legs = Hitbox((width / 2, height / 2 + 80), sans_group, size=(50, 3))
    bombs_on_screen = []
    pygame.mouse.set_pos((width + oleg.width) / 2, (height + oleg.height) / 2)
    cursor = Cursor(*map(lambda x: x / 2, SCREEN_SIZE), cursor_group)
    pygame.mouse.set_visible(True)
    create_starfield(platform_group)
    # Clock init
    clock = pygame.time.Clock()


points = 0  # Счёт игрока
dynamic_points = 0  # То же самое, что points, но обнуляется каждые DYNAMIC_POINTS_LIMIT очков, создавая платформу
if __name__ == '__main__':
    # Pygame and screen initialization
    pygame.init()
    pygame.display.set_caption('Doodle Moodle')
    size = width, height = SCREEN_SIZE
    screen = pygame.display.set_mode(size)
    difficulty_clicks = 0
    interface_running = True
    running = True

    # Sprite groups, start screen and character initialization
    background_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    sans_group = pygame.sprite.Group()
    cursor_group = pygame.sprite.Group()
    spike_group = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()
    timer_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()

    # Milcanceuos (Как это слово пишется?) init

    init_interface(buttons_group)

    screen.fill((255, 255, 255))
    while running:

        while interface_running:
            interface_running = interface()
        pygame.mouse.set_visible(False)
        tick = clock.tick(200)
        # Events reading
        running = buttons_interaction(oleg, legs)

        # Character movement
        move(oleg, sans_group.sprites()[0])
        oleg.change_character_sprite()
        move(legs, sans_group.sprites()[1], True)

        move_platforms(oleg)
        sans_is_dead = bomb_detonation()

        # Collision
        try:
            if oleg.vert_velocity >= 0:
                if pygame.sprite.spritecollideany(sans_group.sprites()[1], platform_group):
                    legs.collision(STANDARD_JUMP_SPEED)
                    oleg.collision(STANDARD_JUMP_SPEED)
            if pygame.sprite.spritecollideany(sans_group.sprites()[0], spike_group):
                sans_group.sprites()[0].kill()
                sans_is_dead = True
                sans_group.sprites()[1].kill()
            for spike in spike_group:
                while pygame.sprite.spritecollideany(spike, platform_group):
                    pygame.sprite.spritecollideany(spike, platform_group).kill()
                    spawn_platform(platform_group)
        except IndexError:
            pass

        # Gravitation
        oleg.vert_velocity += 0.02 * GRAVITATION / 100
        legs.vert_velocity += 0.02 * GRAVITATION / 100
        if abs(oleg.vert_velocity) < STOP_FLOATING_POINT:  # Определяет, при каком значении скорости Санс сразу полетит вниз
            oleg.vert_velocity = 1
            legs.vert_velocity = 1

        killing_sprites()
        if sans_is_dead:
            pygame.mouse.set_visible(True)
            interface_running = True
        render()
pygame.quit()
