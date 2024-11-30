import pygame
from pygame.locals import *

class Image():

    def __init__(self, screen, image_name):

        self._image = pygame.image.load(image_name)
        self._width = self._image.get_width()
        self._height = self._image.get_height()
        self._screen = screen

    def draw(self, left, top, width):
        height = width * self._height / self._width
        image_scaled = pygame.transform.scale(self._image, (width,height))
        self._screen.blit(image_scaled, (left, top))

