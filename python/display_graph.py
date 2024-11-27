import pygame
from math import *
from pygame.locals import *
import numpy as np
import color_map


class Graph():

    def __init__(self, screen):
        self._screen = screen
        self._text_color = (255, 255, 255)
        self._font_name = 'Tahoma'
        self._font = None
        self._left = None
        self._top = None
        self._width = None
        self._height = None
        self._font = None
        self._text_label = None
        self._text_score = None
        self._value_norm = None
        self._label = None
        self._score = None
        self._threshold = None
        self._enabled = None
        self._data_changed = True
        self._bars_total = 7

    def _update_font_size(self):
        for i in range(1, 200, 1):
            font = pygame.font.SysFont(self._font_name, i)
            test = font.render('A', False, self._text_color)
            if test.get_height() > self._height/16:
                self._font = pygame.font.SysFont(self._font_name, i - 1)
                break

    def _update_text(self):
        self._text_label = []
        self._text_score = []
        for i in range(0, self._bars_total):
            self._text_label.append(self._font.render(self._label[i], False, self._text_color))
            self._text_score.append(self._font.render(self._score[i], False, self._text_color))

    def update_data(self, value_norms, labels, scores, thresholds, enabled):
        self._value_norm = value_norms
        self._label = labels
        self._score = scores
        self._threshold = thresholds
        self._enabled = enabled
        self._data_changed = True

    def _draw_bar(self, position):
        pad = 10
        left = self._left
        top = self._top + position * self._height/self._bars_total + pad
        width = self._width
        height = self._height/self._bars_total - 2*pad

        bd_color = (255,255,255)
        black = (0,0,0)

        if not self._enabled[position]:
            color = (25,25,25)
            bd_color = (50,50,50)
        elif self._value_norm[position] >= self._threshold[position]:
            color = (0,128,0)
        else:
            color = (192,0,0)

        radius = height / 2

        #Draw filled bar
        center = (left + radius, top + radius)
        pygame.draw.circle(self._screen, color, center, radius, 0)
        center = (left + width - radius, top + radius)
        pygame.draw.circle(self._screen, color, center, radius, 0)
        rect = pygame.Rect(left + radius, top, width - 2 * radius, height)
        pygame.draw.rect(self._screen, color, rect, 0)

        width_show = self._width * self._value_norm[position]
        rect = pygame.Rect(left + width_show, top-pad/2, width-width_show, height+pad)
        pygame.draw.rect(self._screen, black, rect, 0)
        x_thresh = self._left + self._width * self._threshold[position]
        pygame.draw.line(self._screen, (100,100,100), (x_thresh, top), (x_thresh, top+height), 3)
        x1 = left + radius
        x2 = left + width - radius
        y = top
        pygame.draw.line(self._screen, bd_color, (x1, y), (x2, y), 1)
        y = top + height
        pygame.draw.line(self._screen, bd_color, (x1, y), (x2, y), 1)
        rect = pygame.Rect(left, top, 2 * radius, height)
        pygame.draw.arc(self._screen, bd_color, rect, pi / 2, -pi / 2, 1)
        rect = pygame.Rect(left + width - 2 * radius, top, 2 * radius, height)
        pygame.draw.arc(self._screen, bd_color, rect, -pi / 2, pi / 2, 1)


        if self._enabled[position]:
            # Draw label text
            text_pos = (left + pad, top + (height - self._text_label[position].get_height()) / 2)
            self._screen.blit(self._text_label[position], text_pos)

            # Draw score text
            text_pos = (left + width - pad - self._text_score[position].get_width(), top + (height - self._text_score[position].get_height()) / 2)
            self._screen.blit(self._text_score[position], text_pos)

    def draw(self, left, top, width, height):
        if width != self._width or left !=self._left:
            self._left = left
            self._top = top
            self._width = width
            self._height = height
            self._update_font_size()
            self._update_text()
        elif self._data_changed:
            # Clear dial by drawing black
            pygame.draw.rect(self._screen,(0,0,0),pygame.Rect(left, top, width, height))

            # Update text
            self._update_text()

        if self._label is not None:
            for i in range(0,self._bars_total):
                self._draw_bar(i)

        # Frame outline
        #color = (255, 255, 255)
        #pygame.draw.rect(self._screen, color, pygame.Rect(left, top, width, height), 1)

