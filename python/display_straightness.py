import math

import pygame
from pygame.locals import *
from math import *


class Plot():

    def __init__(self, screen):
        self._screen = screen

    def draw(self, center, radius, straightness):

        magnitude, angle, threshold = straightness
        center_x, center_y = center

        if (magnitude<=threshold):
            color = (0, 128, 0)
        else:
            color = (192, 0, 0)

        # Draw threshold
        pygame.draw.circle(self._screen, color, center, radius*threshold, 0)

        white = (255,255,255)
        gray = (128, 128, 128)
        pygame.draw.circle(self._screen, white, center, radius, 1)

        for i in range(1,5):
            pygame.draw.circle(self._screen, gray, center, radius*i/5, 1)

        for i in range(0,12):
            x = center[0] + radius * cos(2 * pi * i / 12)
            y = center[1] + radius * sin(2 * pi * i / 12)
            pygame.draw.line(self._screen, gray, center,(x,y))






        # Draw digicue straightness
        color = (0, 255, 255)
        str_r = radius * magnitude
        x = center_x + str_r * math.sin(pi / 180 * angle + pi)
        y = center_y + str_r * -math.cos(pi / 180 * angle + pi)

        pygame.draw.line(self._screen, color, center, (x, y), 3)
        for i in range(-1, 2, 2):
            arrow_r = 40
            if arrow_r > str_r / 3:
                arrow_r = str_r / 3
            xa = x + arrow_r * sin(pi / 180 * (angle + 30 * i))
            ya = y + arrow_r * -cos(pi / 180 * (angle + 30 * i))
            pygame.draw.line(self._screen, color, (x,y), (xa, ya), 3)



