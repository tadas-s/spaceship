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

        overlay = pygame.Surface([WIDTH, HEIGHT])
        overlay.set_alpha(32)
        overlay.fill(BLACK)

        pygame.draw.line(overlay, WHITE, [0, int(HEIGHT / 2)], [WIDTH, int(HEIGHT / 2)])
        pygame.draw.line(overlay, WHITE, [int(WIDTH / 2), 0], [int(WIDTH / 2), HEIGHT])

        for r in range(1, 10):
            pygame.draw.circle(overlay, WHITE, [int(WIDTH / 2), int(HEIGHT / 2)], r * 40, 1)

        while not self.quit.value:
            pygame.draw.line(
                self.window, GREEN,
                [int(WIDTH / 2), int(HEIGHT / 2)],
                [int((HEIGHT / 2)*sin(angle) + WIDTH / 2),
                 int((HEIGHT / 2)*cos(angle) + HEIGHT / 2)],
                5
            )

            self.window.blit(overlay, [0, 0])

            angle += 0.02

            pygame.display.update()
            sleep(0.01)

        pygame.quit()
