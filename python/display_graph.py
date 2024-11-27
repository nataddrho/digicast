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
        self._radius = None
        self._center = None
        self._font_large = None
        self._font_small = None
        self._large_text_surface = None
        self._small_text_surface = None
        self._large_text = ''
        self._small_text = ''
        self._value_norm = 0
        self._data_changed = True

    def _update_font_size(self):
        for i in range(1, 200, 1):
            font = pygame.font.SysFont(self._font_name, i)
            test = font.render('00.00', False, self._text_color)
            if test.get_width() > self._radius:
                self._font_large = pygame.font.SysFont(self._font_name, i - 1)
                s = int((i-1)*.5)
                if s < 0:
                    s = 1
                self._font_small = pygame.font.SysFont(self._font_name, s)
                break

    def _update_large_text(self):
        self._large_text_surface = self._font_large.render(self._large_text, False, self._text_color)

    def _update_small_text(self):
        self._small_text_surface = self._font_small.render(self._small_text, False, self._text_color)

    def _draw_dial_arc(self,value_norm):
        zero_deg = -90
        range_deg = 340
        segments = 100
        length_deg = range_deg / segments
        v = value_norm
        if v>1.0:
            v = 1.0
        elif v<0:
            v=0
        for i in range(0,segments):
            f = i/(segments-1)
            if f>v:
                break
            start_deg = zero_deg + length_deg*i
            color = color_map.cmap[round(f*100)][:3]
            self._draw_dial_arc_segment(start_deg, length_deg, color)

    def _draw_dial_arc_segment(self, start_deg, length_deg, color):
        radius = self._radius
        center_x, center_y = self._center
        polygons = []
        N=10
        theta = start_deg * pi / 180
        phi = length_deg * pi / 180
        r1 = radius
        r2 = radius*0.66
        x = center_x - r2 * cos(theta)
        y = center_y - r2 * sin(theta)
        coordinates = [(x,y)]
        x = center_x - r1 * cos(theta)
        y = center_y - r1 * sin(theta)
        coordinates.append((x,y))
        for i in range(0,N+1):
            x = center_x - r1 * cos(phi * i / N + theta)
            y = center_y - r1 * sin(phi * i / N + theta)
            coordinates.append((x,y))
        for i in range(0,N):
            x = center_x - r2 * cos(phi * (N-i) / N + theta)
            y = center_y - r2 * sin(phi * (N-i) / N + theta)
            coordinates.append((x,y))

        polygon = ((color, coordinates, False))
        polygons.append(polygon)

        for poly in polygons:
            pygame.draw.polygon(self._screen, *poly)

    def update_data(self, value_norm, large_text, small_text):
        self._value_norm = value_norm
        self._large_text = large_text
        self._small_text = small_text
        self._data_changed = True

    def draw(self, center, radius):
        if radius != self._radius or center!=self._center:
            self._radius = radius
            self._center = center
            self._update_font_size()
            self._update_large_text()
            self._update_small_text()
        elif self._data_changed:
            # Clear dial by drawing black
            center_x, center_y = self._center
            rect = pygame.Rect((center_x - radius, center_y - radius), (2*radius, 2*radius))
            pygame.draw.rect(self._screen,(0,0,0),rect)

            # Update text
            self._update_large_text()
            self._update_small_text()

        center_x, center_y = self._center
        self._draw_dial_arc(self._value_norm)
        white = (255, 255, 255)
        pygame.draw.circle(self._screen, white, center, radius + 1, 1)
        text_pos = (center_x - self._large_text_surface.get_width() / 2, center_y - self._large_text_surface.get_height() / 2)
        self._screen.blit(self._large_text_surface, text_pos)
        text_pos = (center_x - self._small_text_surface.get_width() / 2, center_y - self._small_text_surface.get_height() / 2 + self._large_text_surface.get_height() / 2 + 10)
        self._screen.blit(self._small_text_surface, text_pos)
