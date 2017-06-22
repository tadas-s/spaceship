from multiprocessing import Process
from time import sleep
import pygame
from math import sin, cos, pi

# Usable screen area (rest is hidden by the front panel)
LEFT = 125
TOP = 5
WIDTH = 575
HEIGHT = 570

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (70, 255, 10)

# TODO: https://www.pygame.org/docs/ref/surface.html#pygame.Surface.subsurface
# Use subsurface.

class Display(Process):
    def __init__(self, logger=None, quit_flag=None):
        self.logger = logger
        self.quit = quit_flag
        super(Display, self).__init__()

    def run(self):
        pygame.init()

        self.window = \
            pygame.display.set_mode((800, 600), 0, 32).subsurface((LEFT, TOP, WIDTH, HEIGHT))

        angle = 0.0

        cleaner = pygame.Surface([WIDTH, HEIGHT])
        cleaner.set_alpha(64)
        cleaner.fill(BLACK)

        while not self.quit.value:
            self.window.blit(cleaner, [0, 0])

            pygame.draw.line(
                self.window, GREEN,
                [int(WIDTH / 2), int(HEIGHT / 2)],
                [int((HEIGHT / 2)*sin(angle) + WIDTH / 2), int((HEIGHT / 2)*cos(angle) + HEIGHT / 2)],
                5
            )

            angle += 0.1

            pygame.draw.line(self.window, WHITE, [0, int(HEIGHT / 2)], [WIDTH, int(HEIGHT / 2)])
            pygame.draw.line(self.window, WHITE, [int(WIDTH / 2), 0], [int(WIDTH / 2), HEIGHT])

            for r in range(1, 10):
                pygame.draw.circle(self.window, WHITE, [int(WIDTH / 2), int(HEIGHT / 2)], r * 40, 1)
            pygame.display.update()
            sleep(0.05)

        pygame.quit()
