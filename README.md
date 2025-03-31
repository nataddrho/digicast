
# DigiCast
A light-weight Python-based application for Raspberry Pi Zero 2 W (or any other platform that has BLE hardware and can run Python). The program displays information from one or two DigiBalls in real time. This is a BLE straight to HDMI solution.

The DigiBall is a digital billiards ball that measures the accuracy of your stroke so that you can compare it to your intentions. Novice players may not give any thought to the importance of where on the face of the cue ball they hit it, as long as the cue ball makes the object ball go in the pocket. But for any high level of play, it is extremely important. Hitting the ball too much on one side of center will cause it to deflect in the opposite direction of your aiming line, resulting in a miss. Advanced players know this, and use the deviation in combination with deliberate tip offset to both pocket the object ball and spin the cue ball off of the rails into desired positions. But again, deviations in the accuracy of the deliberate off-center tip hits cause poor results. By obtaining real time feedback on where you actually hit the ball and comparing it to where you intended to hit the ball, you can make permanent adjustments quickly.

Version 1.1.0: 11/30/2024 - Now works with the DigiCue
Version 1.1.2: 01/13/2025 - Improved BLE scanning efficiency, smooth counting timer.


See www.digicue.net for more information.

### Requirements:

- Raspberry Pi Zero 2 W
- Micro-SD card (16 GB or greater, 32 GB recommended)
- PC with a micro-SD card reader or USB reader
- Micro HDMI to HDMI cable
- 5VDC Power Adapter (5W or greater)

### Installation:

1. Download the Raspberry Pi Imager software (v1.8.5 used at the time of writing this).

2. Choose Raspberry Pi Zero 2 W for the device.

3. Choose Raspberry Pi OS (64-bit) (recommended) for the operating system.

4. Choose your micro-SD card as the storage solution.

5. Optional: Set up user name and password, and SSH.

6. Build image on micro-SD card

7. Install the card into the Zero 2, plug a mouse and keyboard through a USB hub into the micro-USB port, and power on. Or connect remotely with SSH at digicast@digicast, or if you know the IP address already.

8. Wait for the system to boot into the Desktop. Navigate to Raspberry Pi Configuration and change Boot to CLI. Save and restart. Alternatively, you can open a terminal and perform the same operation by using the ```raspi-config``` command. Reboot by typing ```sudo shutdown -r now```

9. Run an update by running ```sudo apt update```

10. Install the BLE library Bleak by running ```sudo apt install python3-bleak```

11. Clone the digiball-pi repository with ```git clone https://github.com/nataddrho/digicast.git```

12. Create a systemd service. Copy service to systemd: ```sudo cp digicast/digicast.service /lib/systemd/system``` Register the service: ```sudo systemctl daemon-reload``` Tell system to start on boot: ```sudo systemctl enable digicast.service``` 

13. Put the file system into read-only mode by creating an overlay. This protects from corruption caused by turning off the power of the Raspberry Pi abruptly (which is what we want to do). Run ```sudo raspi-config```, navigate to Performance Options, Overlay File System and press enter. Select Yes when prompted to enable the overlay file system. Select Yes when prompted to write-protect the boot partition.

14. Reboot the system.

15. The DigiCast application should start automatically on every power up.

### Generating a Backup Image:

1. Format an SD Card or USB Flash drive (8GB or larger) to NTFS or exFAT. Don't use FAT32 because the individual backup image file size is too small for this format.

2. Use micro-USB adapter and attach a USB-3.0 hub (plugs must be blue) to the Raspberry Pi USB port (to the left of the power port). The USB port and power ports both use micro-USB connectors. You will have to remove the Raspberry Pi from the DigiCast case in order to access this port.

3. Plug in both a keyboard and a micro SD card reader (or USB Flash drive) to the hub.  

3. Power on unit. Wait for DigiCast splash screen to appear with DigiBall/DigiCue/Aramith logos.

4. Press the Backspace key once and wait for the prompt to appear.

5. Log in with username and password.

6. Type ```lsblk``` to show the available devices for mounting. The SD Card / Flash drive will usually appear as /dev/sda1

7. Make a mounting directory by typing ```sudo mkdir /mnt/backup```

8. Mount your media by typing ```sudo mount /dev/sdaX /mnt/backup``` where X is the number of your device.

9. Navigate to the backup utilities ```cd digicast/image-utils```

10. Set scripts to executable ```sudo chmod +x image*```

11. Start backup process. This will take an hour or two to complete with no immediate feedback messages: ```sudo ./image-backup --initial /mnt/backup/image.img```

12. When complete, check image ```sudo ./image-check /mnt/backup/image.img```

13. Unmount device by typing ```sudo umount /dev/sdaX``` where X is the number of your device.

### How to Use:

Plug the raspberry pi into the TV and power. Allow the device to finish booting. You should see the following message: 

![alt text](https://github.com/nataddrho/digiball-pi/blob/master/pictures/waiting.jpg?raw=true)

Turn on a DigiBall by moving it/shooting with it. Then bring it close to the raspberry pi to connect. The pi will remain connected to this DigiBall until the pi is turned off.

![alt text](https://github.com/nataddrho/digiball-pi/blob/master/pictures/oneplayer.jpg?raw=true)

If you have more than one carom DigiBall, you can add a second player by bringing a second DigiBall close to the pi. The screen will change to show two players.

![alt text](https://github.com/nataddrho/digiball-pi/blob/master/pictures/twoplayers.jpg?raw=true)

The signal strength (RSSI in dBm) is shown as faint grey numbers at the upper corner of the screen. A good signal strength is anything greater than -90. -100 or less would suggest poor reception. Note: To connect a DigiBall to the pi, it ball needs to be brought close enough to have a signal strength of -55 dBm or more.

![alt text](https://github.com/nataddrho/digiball-pi/blob/master/pictures/rssi.jpg?raw=true)

The Raspberry PI Zero 2 W can be ordered from many locations including Amazon, DigiKey, Mouser, etc. See list of distributors at raspberrypi.com. Many vendors make kits with cases and adapters.

![alt text](https://github.com/nataddrho/digiball-pi/blob/master/pictures/zero-2.jpg?raw=true)

![alt text](https://github.com/nataddrho/digiball-pi/blob/master/pictures/size.jpg?raw=true)

