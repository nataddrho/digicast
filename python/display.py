import pygame
from math import *
from pygame.locals import *
import display_dial
import display_ball
import display_graph


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

    return [x, y, 0.9 * r]


class Scaffold():

    def __init__(self, ball_type):

        self._frames = 1  # can be 1 or 2
        self._ball_pad = 25
        self._ball_type = ball_type

        self._width = 1920
        self._height = 1080

        self._digiball_data = [None, None]
        self._digicue_data = [None, None]

        # Define the dimensions of screen object
        self._screen = pygame.display.set_mode((self._width, self._height),
                                               pygame.RESIZABLE)

        # Clear screen
        self._screen.fill((0, 0, 0))

        self._frame_objects = []
        for i in range(0, 2):
            objects = []
            objects.append(display_ball.Ball(self._screen, self._ball_type, i == 1))
            objects.append(display_dial.Dial(self._screen))
            objects.append(display_dial.Dial(self._screen))
            objects.append(display_dial.Dial(self._screen))
            objects.append(display_dial.Dial(self._screen))
            objects.append(display_graph.Graph(self._screen))
            self._frame_objects.append(objects)

    def update_size(self, width, height):
        self._width = width
        self._height = height

    def update_data(self, digiball_data, digicue_data):

        clearScreen = False
        for i in range(0, 2):
            if self._digiball_data[i] is None and digiball_data[i] is not None:
                clearScreen = True
            if self._digicue_data[i] is None and digicue_data[i] is not None:
                clearScreen = True

        if clearScreen:
            self._screen.fill((0, 0, 0))

        if digiball_data is not None:
            self._digiball_data = digiball_data
            if digiball_data[1] is not None:
                if (self._frames) != 2:
                    self._frames = 2

        if digicue_data is not None:
            self._digicue_data = digicue_data
            if digicue_data[1] is not None:
                if (self._frames) != 2:
                    self._frames = 2

    def _draw_rssi(self, rssi_text, frame_left, frame_top):
        # RSSI
        font = pygame.font.SysFont("Tahoma", 18)
        fs = font.render(rssi_text, False, (80, 80, 80))
        pygame.draw.rect(self._screen, (0, 0, 0), pygame.Rect(frame_left, frame_top, fs.get_width(), fs.get_height()))
        self._screen.blit(fs, (frame_left, frame_top))

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

            ball_radius_optimized = min(width, height) / 2 - self._ball_pad

            if frame == 0:
                ret = optimize_circle_placement(center_x, center_y, ball_radius_optimized)
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

            ball, spin, tip, speed, time, graph = self._frame_objects[frame]

            player1_digiball = self._digiball_data[0] is not None
            player2_digiball = self._digiball_data[1] is not None
            player1_digicue = self._digicue_data[0] is not None
            player2_digicue = self._digicue_data[1] is not None
            device_found = player1_digicue or player2_digicue or player1_digiball or player2_digiball

            if frame == 0 and not device_found:
                # Message
                font = pygame.font.SysFont("Tahoma", 48)
                fs = font.render('Move DigiBall/DigiCue close to receiver to connect...', False, (255, 255, 255))
                text_pos = (center_x - fs.get_width() / 2,
                            center_y - fs.get_height() / 2)
                self._screen.blit(fs, text_pos)

            else:

                digiball_data = self._digiball_data[frame]
                digicue_data = self._digicue_data[frame]
                digiball_present = digiball_data is not None
                digicue_present = digicue_data is not None

                if digiball_present or digicue_present:

                    if digicue_present:
                        # DigiBall Graph
                        graph.update_data(0.5, "99", "test")
                        center = (left + width / 2, top + height / 2)
                        graph.draw(center, dial_radius)

                    if digiball_present:

                        tip_percent = digiball_data["Tip Percent"]
                        tip_percent = round(tip_percent / 5) * 5  # precision of 5 percent
                        tip_angle = digiball_data["Tip Angle"]

                        # Ball
                        center = (center_x, center_y)
                        ball.draw(center, ball_radius_optimized, tip_angle, tip_percent)

                        # Spin
                        center = (left + dial_offset_x, top + dial_offset_y)
                        spin_rps = digiball_data["Spin RPS"]
                        spin_text = "%.1f" % spin_rps
                        if digiball_data["Gyro Clipping"]:
                            spin_text = "%s+" % spin_text
                        spin.update_data(spin_rps / 15, spin_text, "RPS")
                        spin.draw(center, dial_radius)

                        # Tip Offset
                        center = (left + width - dial_offset_x, top + dial_offset_y)

                        tip.update_data(tip_percent / 55, "%i" % tip_percent, "PFC")
                        tip.draw(center, dial_radius)

                        # Speed
                        center = (left + dial_offset_x, top + height - dial_offset_y)
                        speed_kmph = digiball_data["Speed KMPH"]
                        speed_kmph = round(speed_kmph * 2) / 2  # precision 0f 0.5 mph
                        speed_text = "%.1f" % speed_kmph
                        if (speed_kmph > 7):
                            speed_text = "%s+" % speed_text
                        speed.update_data(speed_kmph / 12, speed_text, "KM/H")
                        speed.draw(center, dial_radius)

                        # Time
                        time_sec = digiball_data["Motionless"]
                        charging = digiball_data["Charging"]
                        if charging == 1:
                            time.update_data(0, "CHARGE", "BATTERY")
                        elif charging == 2:
                            time.update_data(0, "CHARGE", "ERROR")
                        elif charging == 3:
                            time.update_data(1, "CHARGE", "COMPLETE")
                        else:
                            time.update_data(time_sec / 300, "%i" % time_sec, "SEC")
                        center = (left + width - dial_offset_x, top + height - dial_offset_y)
                        time.draw(center, dial_radius)

                # RSSI
                if digiball_present and digicue_present:
                    rssi_text = "%i/%i" % (digiball_data["RSSI"], digicue_data["RSSI"])
                elif digiball_present:
                    rssi_text = "%i" % digiball_data["RSSI"]
                else:
                    rssi_text = "%i" % digicue_data["RSSI"]
                self._draw_rssi(rssi_text, left, top)
