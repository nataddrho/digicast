import pygame
from math import *
from pygame.locals import *
import display_dial
import display_ball


def optimize_circle_placement(center_x, center_y, ball_radius):
    Z = sqrt(center_x ** 2 + center_y ** 2)
    x = 1 / (2 * sqrt(2)) * (Z - ball_radius)
    y = x
    r = sqrt(2) * x
    if (x - r) < 0:
        r = x
    if (y - r) < 0:
        r = y
    if (x + r) > center_x:
        r = center_x - x
    if (y + r) > center_y:
        r = center_y - y
    if (center_x - ball_radius - 2 * r) > 0:
        x = (center_x - ball_radius) / 2
    if (center_y - ball_radius - 2 * r) > 0:
        y = (center_y - ball_radius) / 2
    dx = x - r
    dy = y - r

    if 0 < dy < dx:
        r = r + dy / 2
        y = y - dy / 2

    if 0 < dx < dy:
        r = r + dx / 2
        x = x - dx / 2

    return [x, y, 0.9*r]


class Scaffold():

    def __init__(self):

        self._frames = 1 # can be 1 or 2
        self._ball_pad = 25

        self._width = 800
        self._height = 400

        self._digiball_data = None

        # Define the dimensions of screen object
        self._screen = pygame.display.set_mode((self._width, self._height),
                                               pygame.RESIZABLE)

        self._frame_objects = []
        for i in range(0, self._frames):
            objects = []
            objects.append(display_ball.Ball(self._screen, i == 1))
            objects.append(display_dial.Dial(self._screen))
            objects.append(display_dial.Dial(self._screen))
            objects.append(display_dial.Dial(self._screen))
            objects.append(display_dial.Dial(self._screen))
            self._frame_objects.append(objects)

    def update_size(self, width, height):
        self._width = width
        self._height = height

    def update_data(self, digiball_data):
        if digiball_data is not None:
            self._screen.fill((0, 0, 0))
            self._digiball_data = digiball_data

    def draw(self):

        # Draw complications and ball displays
        dial_offset_x, dial_offset_y, dial_radius = (0, 0, 1)
        for frame in range(self._frames):
            width = self._width / self._frames
            height = self._height
            left = width * frame
            top = 0
            center_x = left + width / 2
            center_y = top + height / 2

            ball_radius = min(width, height) / 2 - self._ball_pad

            if frame == 0:
                ret = optimize_circle_placement(center_x, center_y, ball_radius)
                dial_offset_x, dial_offset_y, dial_radius = ret

            """
            # Frame outline
            color = (255, 255, 255)
            pygame.draw.rect(self.screen, color, pygame.Rect(left, top, left + width, top + height), 1)

            # Complication outline
            pygame.draw.circle(self.screen, color, (left + dial_offset_x, top + dial_offset_y), dial_radius, 1)
            pygame.draw.circle(self.screen, color, (left + width - dial_offset_x, top + dial_offset_y), dial_radius, 1)
            pygame.draw.circle(self.screen, color, (left + dial_offset_x, top + height - dial_offset_y), dial_radius, 1)
            pygame.draw.circle(self.screen, color, (left + width - dial_offset_x, top + height - dial_offset_y), dial_radius, 1)

            # Ball outline
            pygame.draw.circle(self.screen, color, (center_x, center_y), ball_radius, 1)
            """

            ball, spin, tip, speed, time = self._frame_objects[frame]

            # Ball
            center = (center_x, center_y)

            if self._digiball_data is None:
                #No data. Just draw ball
                ball.draw(center, ball_radius)
            else:

                tip_percent = self._digiball_data["Tip Percent"]
                tip_percent = round(tip_percent / 5) * 5  # precision of 5 percent
                tip_angle = self._digiball_data["Tip Angle"]

                # Ball
                ball.draw(center, ball_radius, tip_angle, tip_percent)

                # Spin
                center = (left + dial_offset_x, top + dial_offset_y)
                spin_rpm = self._digiball_data["Spin RPM"]
                spin.update_data(spin_rpm/1000,"%i"%spin_rpm,"RPM")
                spin.draw(center, dial_radius)

                # Tip Offset
                center = (left + width - dial_offset_x, top + dial_offset_y)

                tip.update_data(tip_percent/55, "%i"%tip_percent, "PFC")
                tip.draw(center, dial_radius)

                # Speed
                center = (left + dial_offset_x, top + height - dial_offset_y)
                speed_mph = self._digiball_data["Speed MPH"]
                speed_mph = round(speed_mph * 2) / 2 # precision 0f 0.5 mph
                speed_text = "%.1f"%speed_mph
                if (speed_mph>7):
                    speed_text = "%s+"%speed_text
                speed.update_data(speed_mph / 8,speed_text,"MPH")
                speed.draw(center, dial_radius)

                # Time
                time_sec = self._digiball_data["Motionless"]
                time.update_data(time_sec/300,"%i"%time_sec,"SEC")
                center = (left + width - dial_offset_x, top + height - dial_offset_y)
                time.draw(center, dial_radius)



