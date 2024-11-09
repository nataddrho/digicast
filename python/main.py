#!/usr/bin/env python
import pygame
from pygame.locals import *
import display
import threading
import queue
import time
from bleak import BleakScanner
import asyncio
import struct
from math import *
import sys

class BLE_async():

    def __init__(self):
        self._devices = None
        self._done = True
        self._last_shot_number = -1
        self.mac_addresses = [None,None]

    async def _scan(self):
        self._devices = await BleakScanner.discover(2.0, return_adv=True, scanning_mode="passive")

    def _digiball_parser(self, devices):

        ball_data = [None, None]

        for mac_address in devices:
            d = devices[mac_address][1]
            rssi = d.rssi
            manuf = d.manufacturer_data
            for manuf_id in manuf:

                if manuf_id == 0x03DE: #NRLLC

                    mdata = manuf[manuf_id]
                    device_type = int(mdata[3])

                    if device_type==1: #DigiBall device type is always 1

                        # Save device as target if brought close to receiver
                        rssi_range = -55
                        if self.mac_addresses[0] is None and rssi>rssi_range:
                            self.mac_addresses[0] = mac_address
                        elif self.mac_addresses[1] is None and rssi>rssi_range and mac_address!=self.mac_addresses[0]:
                            self.mac_addresses[1] = mac_address

                        if mac_address in self.mac_addresses:

                            if mac_address == self.mac_addresses[0]:
                                player = 1
                            else:
                                player = 2

                            data_ready = (int(mdata[17]) >> 6) == 1;
                            shot_number = int(mdata[6]) & 0x3F

                            if data_ready:
                                data = {}
                                data["RSSI"] = rssi
                                data["MAC Address"] = mac_address
                                data["Charging"] = int(mdata[7])>>6
                                data["Gyro Clipping"] = (int(mdata[6])>>7)==1
                                data["Motionless"] = (int(mdata[7]) & 0x03) + int(mdata[8])
                                data["Shot Number"] = shot_number
                                data["Tip Percent"] = int(mdata[11])
                                speed_factor = int(mdata[12])
                                spin_horz_dps = struct.unpack('>h', mdata[13:15])[0]
                                spin_vert_dps = struct.unpack('>h', mdata[15:17])[0]
                                spin_mag_rpm = sqrt(spin_horz_dps ** 2 + spin_vert_dps ** 2) / 6
                                data["Speed KMPH"] = 0.06 * 1.60934 * speed_factor
                                spin_degrees = 180 / pi * atan2(spin_horz_dps, spin_vert_dps)
                                data["Spin RPS"] = spin_mag_rpm/60
                                data["Tip Angle"] = spin_degrees

                                ball_data[player-1] = data
        return ball_data


    def async_task(self,q):
        try:
            asyncio.run(self._scan())
            q.put(self._digiball_parser(self._devices))
        except:
            pass


def gui_main(ball_type):

    ble = BLE_async()
    q = queue.Queue()

    thread = threading.Thread(target=ble.async_task, args=(q,))
    thread.start()

    # initialize pygame
    pygame.init()
    pygame.font.init()

    scaffold = display.Scaffold(ball_type)

    pygame.mouse.set_visible(False)

    # Variable to keep our game loop running
    gameOn = True

    # Our game loo
    i = 0
    while gameOn:
        # for loop through the event queue
        for event in pygame.event.get():

            # Check for KEYDOWN event
            if event.type == KEYDOWN:

                if event.key == K_BACKSPACE:
                    gameOn = False

            # Check for QUIT event
            elif event.type == QUIT:
                gameOn = False

            # Check for window resize
            elif event.type == VIDEORESIZE:
                scaffold.update_size(event.w, event.h)


        if not q.empty():
            digiball_data = q.get()
            if digiball_data[0] is not None or digiball_data[1] is not None:

                # Update display information. Needs MAC filtering
                scaffold.update_data(digiball_data)


            thread = threading.Thread(target=ble.async_task, args=(q,))
            thread.start()

        scaffold.draw()
        pygame.display.flip()




if __name__ == '__main__':

    if "carom" in sys.argv:
        ball_type = "carom"
    elif "snooker" in sys.argv:
        ball_type = "snooker"
    else:
        ball_type = "pool"

    print("Nathan Rhoades LLC, 11/9/2024")
    print("digiball-pi: %s" % ball_type)
    gui_main(ball_type)

