from random import randrange
import pygame
from platform import Sas

def create_starfield():



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
                oleg = Sas(randrange(400), randrange(600), all_spice)
                all_spice.draw(screen)
                print("oleg")

        pygame.display.flip()
    pygame.quit()
