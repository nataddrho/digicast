import pygame
from math import *
from pygame.locals import *
import display_dial
import display_ball
import display_graph
import display_plot
import display_image
import version

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

    def __init__(self):

        self._frames = 1  # can be 1 or 2
        self._ball_pad = 25

        self._width = 1920
        self._height = 1080

        self._digiball_data = [None, None]
        self._digicue_data = [None, None]

        # Define the dimensions of screen object
        self._screen = pygame.display.set_mode((self._width, self._height),
                                               pygame.RESIZABLE)

        # Clear screen
        self._screen.fill((0, 0, 0))

        self._digicue_logo = display_image.Image(self._screen, "assets/digicue_blue_logo.png")
        self._digiball_logo = display_image.Image(self._screen, "assets/digiball_logo.png")
        self._aramith_logo = display_image.Image(self._screen, "assets/aramith_logo.png")

        self._frame_objects = []
        for i in range(0, 2):
            objects = []
            objects.append(display_ball.Ball(self._screen))
            objects.append(display_dial.Dial(self._screen))
            objects.append(display_dial.Dial(self._screen))
            objects.append(display_dial.Dial(self._screen))
            objects.append(display_dial.Dial(self._screen))
            objects.append(display_graph.Graph(self._screen))
            objects.append(display_plot.Plot(self._screen))
            self._frame_objects.append(objects)

    def update_size(self, width, height):
        self._width = width
        self._height = height

    def update_data(self, digiball_data, digicue_data, force_screen_clear=False):

        clearScreen = force_screen_clear
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
        fs = font.render(rssi_text, True, (80, 80, 80))
        top = frame_left
        left = frame_top-fs.get_height()
        pygame.draw.rect(self._screen, (0, 0, 0), pygame.Rect(top, left, fs.get_width(), fs.get_height()))
        self._screen.blit(fs, (top, left))

    def draw(self):
        player1_digiball = self._digiball_data[0] is not None
        player2_digiball = self._digiball_data[1] is not None
        player1_digicue = self._digicue_data[0] is not None
        player2_digicue = self._digicue_data[1] is not None
        device_found = player1_digicue or player2_digicue or player1_digiball or player2_digiball

        # Draw complications and ball displays
        dial_offset_x, dial_offset_y, dial_radius = (0, 0, 1)
        for frame in range(self._frames):
            digiball_data = self._digiball_data[frame]
            digicue_data = self._digicue_data[frame]
            digiball_present = digiball_data is not None
            if digiball_present:
                digiball_present = "MAC Address" in digiball_data
            digicue_present = digicue_data is not None
            if digicue_present:
                digicue_present = "MAC Address" in digicue_data

            width_digiball = self._width / self._frames
            width_digicue = 0
            if digiball_present and digicue_present:
                width_digicue = width_digiball * 1/3
                width_digiball *= 2/3
            elif digicue_present:
                width_digiball *= 1/2
                width_digicue = width_digiball

            height = self._height
            left = self._width/2 * frame
            top = 0
            center_x = left + width_digiball / 2
            center_y = top + height / 2
            ball_radius_optimized = min(width_digiball, height) / 2 - self._ball_pad

            ball, spin, tip, speed, time, graph, plot = self._frame_objects[frame]

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

            if frame == 0 and not device_found:
                #Logos
                logo_width = 2 * dial_offset_x
                self._digicue_logo.draw(5,5,logo_width-10)
                self._digiball_logo.draw(self._width-logo_width-5, 5, logo_width-10)
                self._aramith_logo.draw((self._width-logo_width)/2+5,5,logo_width-10)

                # Instructions
                font = pygame.font.SysFont("Tahoma", 56)
                fs = font.render('Touch device to receiver to connect...', True, (255, 255, 255))
                text_pos = (center_x - fs.get_width() / 2,
                            center_y - fs.get_height() / 2)
                pygame.draw.rect(self._screen,(0,0,0),(text_pos[0],text_pos[1],fs.get_width(),fs.get_height()))
                self._screen.blit(fs, text_pos)

                # Version
                font = pygame.font.SysFont("Tahoma", 40)
                fs = font.render("DigiCast\u2122 version %s (%s)"%(version.version, version.date), True, (255, 255, 255))
                text_pos = (center_x - fs.get_width() / 2,
                            self._height - 3* fs.get_height() / 2)
                pygame.draw.rect(self._screen, (0, 0, 0), (text_pos[0], text_pos[1], fs.get_width(), fs.get_height()))
                self._screen.blit(fs, text_pos)

            else:

                if digiball_present or digicue_present:

                    if digicue_present:
                        magnitude = 1 - digicue_data["Straightness"]
                        angle = digicue_data["Straightness Angle"]
                        threshold = 1 - digicue_data["Straightness Threshold"]
                        straightness = (magnitude, angle, threshold)
                    else:
                        straightness = None

                    if digicue_present:
                        # DigiBall Graph
                        labels = ["Finish","Straightness","Tip Steer","Follow Through","Jab","Backstroke Pause","Shot Interval"]
                        values_norm = len(labels)*[None]
                        scores = len(labels)*[None]
                        thresholds = len(labels)*[None]
                        enabled = len(labels)*[None]
                        for i in range(0,len(labels)):
                            label = labels[i]
                            values_norm[i] = digicue_data[label]
                            scores[i] = digicue_data["%s Text"%label]
                            thresholds[i] = digicue_data["%s Threshold"%label]
                            enabled[i] = digicue_data["%s Enabled"%label]

                        graph.update_data(values_norm, labels, scores, thresholds, enabled)
                        graph.draw(left + width_digiball + 10, top + 10, width_digicue - 20, height - 20)

                    if not digiball_present:

                        #Draw plot
                        center = (center_x, center_y)
                        plot.draw(center, ball_radius_optimized, straightness)

                        #Draw logo
                        logo_width = 2 * dial_offset_x
                        self._digicue_logo.draw(5+left, 5, logo_width - 10)

                    else:

                        # Draw ball
                        tip_percent = digiball_data["Tip Percent"]
                        tip_percent = round(tip_percent / 5) * 5  # precision of 5 percent
                        tip_angle = digiball_data["Tip Angle"]
                        ball_diameter = digiball_data["Ball Diameter"]
                        ball_yellow = digiball_data["Ball Color"]=="Yellow"
                        tip_diameter = digiball_data["Tip Diameter"]
                        tip_curvature = digiball_data["Tip Curvature"]

                        center = (center_x, center_y)
                        ball.draw(center, ball_radius_optimized, ball_diameter, ball_yellow, tip_diameter,
                                  tip_curvature, tip_angle, tip_percent, straightness)

                        # Spin
                        center = (left + dial_offset_x, top + dial_offset_y)
                        spin_rps = digiball_data["Spin RPS"]
                        spin_text = "%.1f" % spin_rps
                        if digiball_data["Gyro Clipping"]:
                            spin_text = "%s+" % spin_text
                        spin.update_data(spin_rps / 15, spin_text, "RPS")
                        spin.draw(center, dial_radius)

                        # Tip Offset
                        center = (left + width_digiball - dial_offset_x, top + dial_offset_y)

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
                        center = (left + width_digiball - dial_offset_x, top + height - dial_offset_y)
                        time.draw(center, dial_radius)


                # RSSI
                rssi_text = "ERROR"
                if digiball_present and digicue_present:
                    rssi_text = "%i/%i" % (digiball_data["RSSI"], digicue_data["RSSI"])
                elif digiball_present:
                    rssi_text = "%i" % digiball_data["RSSI"]
                else:
                    rssi_text = "%i" % digicue_data["RSSI"]
                self._draw_rssi(rssi_text, left, top+height)
