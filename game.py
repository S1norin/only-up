from random import randrange
import pygame
from platform import Sas

def create_starfield():
    for y in range(10, 590, 80):
        x = randrange(400)
        oleg = Sas(x, y, all_spice)
        oleg1 = Sas(x + 80, y, all_spice)
        oleg2 = Sas(x - 80, y, all_spice)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Doodle Moodle')
    size = width, height = 400, 600
    screen = pygame.display.set_mode(size)
    running = True
    while running:
        all_spice = pygame.sprite.Group()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    print('here')
                    screen.fill((0, 0, 0))
                    for sprite in all_spice:
                        sprite.rect = sprite.rect.move(sprite.rect.x + 10, sprite.rect.y )

                else:
                    # oleg in his heaven, all's right with project
                    # oleg = Sas(randrange(400), randrange(600), all_spice)

                    create_starfield()

                all_spice.draw(screen)


        pygame.display.flip()
    pygame.quit()
