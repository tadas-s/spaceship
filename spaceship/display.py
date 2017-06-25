from .base_process import BaseProcess
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


class Display(BaseProcess):

    def __init__(self, logger=None, quit_flag=None):
        super(Display, self).__init__(logger=logger, quit_flag=quit_flag)

    def run(self):
        pygame.init()

        self.window = \
            pygame.display.set_mode((800, 600), 0, 32).subsurface((LEFT, TOP, WIDTH, HEIGHT))

        angle = 0.0
        line_width = 5
        overlay_alpha = 32
        speed = 0.01

        overlay = pygame.Surface([WIDTH, HEIGHT])
        overlay.set_alpha(overlay_alpha)
        overlay.fill(BLACK)

        pygame.draw.line(overlay, WHITE, [0, int(HEIGHT / 2)], [WIDTH, int(HEIGHT / 2)])
        pygame.draw.line(overlay, WHITE, [int(WIDTH / 2), 0], [int(WIDTH / 2), HEIGHT])

        for r in range(1, 10):
            pygame.draw.circle(overlay, WHITE, [int(WIDTH / 2), int(HEIGHT / 2)], r * 40, 1)

        while not self.quit():
            if not self.incoming.empty():
                msg = self.incoming.get_nowait()
                if msg[0] == 'analog_1':
                    line_width = msg[1] * 5
                if msg[0] == 'analog_2':
                    overlay_alpha = msg[1] * 32
                if msg[0] == 'analog_3':
                    speed = msg[1] * 0.02

            pygame.draw.line(
                self.window, GREEN,
                [int(WIDTH / 2), int(HEIGHT / 2)],
                [int((HEIGHT / 2)*sin(angle) + WIDTH / 2),
                 int((HEIGHT / 2)*cos(angle) + HEIGHT / 2)],
                int(line_width)
            )

            overlay.set_alpha(overlay_alpha)
            self.window.blit(overlay, [0, 0])

            angle += speed

            pygame.display.update()
            sleep(0.01)

        pygame.quit()
