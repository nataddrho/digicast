#!/usr/bin/env python
import pygame
from pygame.locals import *
import display
import threading
import queue
import sys
import bluetooth_le
import version


def gui_main():

    ble = bluetooth_le.BLE_async()
    q = queue.Queue()

    thread = threading.Thread(target=ble.async_task, args=(q,))
    thread.start()

    # initialize pygame
    pygame.init()
    pygame.font.init()

    scaffold = display.Scaffold()

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

        if ble.test:
            digiball_data, digicue_data = ble.get_test_data()
            scaffold.update_data(digiball_data, digicue_data)

        elif not q.empty():
            digiball_data, digicue_data = q.get()
            if (digiball_data[0] is not None or digiball_data[1] is not None or
                    digicue_data[0] is not None or digicue_data[1] is not None):

                # Update display information
                force_screen_clear = ble.check_for_new_device()
                scaffold.update_data(digiball_data, digicue_data, force_screen_clear)


        scaffold.draw()
        pygame.display.flip()

    thread.join()

if __name__ == '__main__':
    print("digiball-pi: Version %s (%s)"%(version.version, version.date))
    gui_main()

