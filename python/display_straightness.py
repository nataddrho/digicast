import math

import pygame
from pygame.locals import *
from math import *


class Plot():

    def __init__(self, screen):
        self._screen = screen

    def draw(self, center, radius, angle, value_norm, threshold):

        center_x, center_y = center

        if (value_norm<=threshold):
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



        x = center_x + radius * value_norm * math.sin(180 / pi * angle)
        y = center_y + radius * value_norm * -math.cos(180 / pi * angle)

        pygame.draw.line(self._screen, (0,255,255), center, (x,y), 5)


