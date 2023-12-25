import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Doodle Moodle')
    size = width, height = 400, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()
