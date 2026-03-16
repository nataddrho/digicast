from PIL import Image, ImageDraw
from math import *

class DigiBallImage():

    def __init__(self, output_path, ball_diameter, is_yellow = False):

        self._output_path = output_path
        self._ball_diameter = ball_diameter

        if is_yellow:
            self._ball_image = Image.open("assets/blank_yellow.png").convert("RGBA")
        else:
            self._ball_image = Image.open("assets/blank.png").convert("RGBA")

        width, height = self._ball_image.size
        self._radius = min(width,height)/2
        self._tip_diameter = 11.8 / 25.4
        self._tip_curvature = 0.358

    def draw(self,tip_angle=0,tip_percent=0):

        try:

            # Create ball image and draw
            img = self._ball_image.copy()
            draw = ImageDraw.Draw(img, "RGBA")
            center = (self._radius, self._radius)

            # Create grid
            for i in range(1,7):
                x1 = center[0] - self._radius*i/10
                y1 = center[1] - self._radius*i/10
                x2 = center[0] + self._radius*i/10
                y2 = center[1] + self._radius*i/10
                draw.ellipse([x1,y1,x2,y2], outline="black")
            for i in range(0,12):
                x = center[0] + 0.6 * self._radius * cos(2 * pi * i / 12)
                y = center[1] + 0.6 * self._radius * sin(2 * pi * i / 12)
                draw.line([(x,y),center], fill="black")



            # Calculate tip outline position
            ball_radius = self._ball_diameter / 2
            tip_radius = self._tip_diameter / 2

            tip_radius_curvature_ratio = self._tip_curvature / ball_radius

            t = tip_percent
            if t>55:
                t=55
            r1 = ball_radius * t/100
            draw_offset = r1 * tip_radius_curvature_ratio
            px1 = 0
            s1 = r1 + draw_offset
            if (s1-tip_radius) > r1:
                px1 = r1 + tip_radius
            else:
                px1 = s1

            # Draw tip outline
            color = (0, 0, 0)
            ax = sin(pi / 180 * tip_angle)
            ay = -cos(pi / 180 * tip_angle)
            x = center[0] + self._radius * ax * px1 / ball_radius
            y = center[1] + self._radius * ay * px1 / ball_radius
            tr = self._radius * tip_radius / ball_radius

            alpha = 128
            pos = (x-tr,y-tr,2*tr,2*tr)

            x1 = x - tr
            y1 = y - tr
            x2 = x + tr
            y2 = y + tr

            overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)

            draw.ellipse([x1, y1, x2, y2], fill=(0, 0, 0, alpha))



            #draw.ellipse([x1,y1,x2,y2], fill=(0,0,0,alpha))

            # Calculate tip contact point
            x_contact = center[0] + self._radius * ax * r1 / ball_radius
            y_contact = center[1] + self._radius * ay * r1 / ball_radius
            tr /= 10
            if tr<3:
                tr = 3

            # Draw tip contact point
            dot_radius = 2
            x1 = x_contact - dot_radius
            y1 = y_contact - dot_radius
            x2 = x_contact + dot_radius
            y2 = y_contact + dot_radius

            draw.ellipse([x1,y1,x2,y2], fill=(0, 255, 255, 255))

            img = Image.alpha_composite(img, overlay)

            img.save(self._output_path, format='PNG')

        except:
            pass





#Test
dbimg = DigiBallImage("assets/test.png",2.25,False)

import time, random
while 1:
    time.sleep(1)
    print("writing")
    dbimg.draw(int(360*random.random()),int(55*random.random()))

