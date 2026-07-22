
# DigiCast
A light-weight Python-based application for Raspberry Pi Zero 2 W (or any other platform that has BLE hardware and can run Python). The program displays information from one or two DigiBalls (and DigiCues) in real time. This is a BLE straight to HDMI solution.

The DigiBall is a digital billiards ball that measures the accuracy of your stroke so that you can compare it to your intentions. Novice players may not give any thought to the importance of where on the face of the cue ball they hit it, as long as the cue ball makes the object ball go in the pocket. But for any high level of play, it is extremely important. Hitting the ball too much on one side of center will cause it to deflect in the opposite direction of your aiming line, resulting in a miss. Advanced players know this, and use the deviation in combination with deliberate tip offset to both pocket the object ball and spin the cue ball off of the rails into desired positions. But again, deviations in the accuracy of the deliberate off-center tip hits cause poor results. By obtaining real time feedback on where you actually hit the ball and comparing it to where you intended to hit the ball, you can make permanent adjustments quickly.

 - Version 1.2.1: 05/26/2026 - Fixed DigiCue straightness threshold bug, disabled hotspot by default, single billiard device as default.
 - Version 1.2.0: 03/18/2026 - Added capability to save images to /dev/shm and expose with a hostspot webserver at http://10.42.0.1:5000. Use nmcli to setup hotspot services and enable webserver in bluetooth_le.py.
 - Version 1.1.3: 06/17/2025 - Changed lower left dial from speed to spin angle in clock format.
 - Version 1.1.2: 01/13/2025 - Improved BLE scanning efficiency, smooth counting timer.
 - Version 1.1.0: 11/30/2024 - Now works with the DigiCue

See www.digicue.net for more information.

### Requirements:

- Raspberry Pi Zero 2 W
- Micro-SD card (16 GB or greater, 32 GB recommended. SanDisk Ultra 32GB A1 is a good choice)
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

14. Reboot the system by typing ```reboot```

15. The DigiCast application should start automatically on every power up.

16. Press the Backspace key once and wait for the prompt to appear. Log in.

17. Verify that the overlay file system is enabled with the command ```cat /boot/firmware/cmdline.txt``` and verify that the argument ```overlayroot=tmpfs``` is present.

18. Shutdown the system by typing ```sudo shutdown now```. When powered off you can then remove the SD Card and store or copy the image as you wish.

### Enabling Two-Player Mode:

As of version 1.2.1, two-player mode is disabled by default. This is to reduce accidental scanning of other player's devices when being used in a public environment. To enable two-player mode / split-screen TV of a purchased DigiCast unit, you will need the following tools:

- Torx T8 screw-driver
- Micro-USB male to USB-A female adapter

1. (If applicable) Unscrew the four screws holding the case together. Remove the Raspberry Pi Zero 2 W from the case.

2. Plug a monitor into the HDMI port using the supplied micro-HDMI to HDMI cable, a keyboard into the USB port using the USB adapter, and the supplied AC adapter into the power port.

3. Wait for the device to boot up.

4. When the DigiCast welcome screen appears, press Backspace once. This exits the program.

5. Log into the system with username digicast and password DigiCast1!

6. Type ```sudo raspi-config``` to open the configuration tool. Navigate to Performance Options > Overlay File System and disable the overlay.

7. Exit and type ```sudo reboot``` to reboot the system.

8. Repeat steps 4 and 5 above.

9. Type ```nano digicast/python/main.py```

10. Navigate to line 16 and change ```allow_multiple_devices = False``` to ```True```

11. Press Ctrl-X to exit nano and press Y to save.

12. Exit and type ```sudo reboot``` to reboot the system and repeat steps 4 and 5 above.

13. Type ```sudo raspi-config``` to open the configuration tool. Navigate to Performance Options > Overlay File System and enable the overlay again.

14. Type ```sudo shutdown -h now``` to shutdown the system. Wait for the LED on the Zero 2 to blink 10 times before unplugging the AC adapter.

15. (If applicable) Reasseble the Zero 2 into the case and tighten screws.

### Enabling Shared Image Folder

Ball graphics can be written as images to RAM and shared as read only over the network. This can be useful for generating images for overlays for streaming software such as OBS. Wi-Fi and Bluetooth share the same radio, so it is ideal to install and configure a separate USB Wi-Fi dongle to decrease latency.

1. Open the device, connect and disable both the file system and boot overlay. See steps in Enabling Two-Player Mode above.

2. Type ```sudo nmtui``` and connect to your desired network for sharing.

3. Type ```sudo apt update``` and then ```sudo apt install samba``` (assuming that you have an internet connection).

4. Create a Samba user by typing ```sudo smbpasswd -a digicast``` and enter DigiCast1!, or any other user/password you want.

5. Type ```sudo nano /etc/samba/smb.conf``` to edit the configuration file. Add the following section to the end of the file:

```
[digiball]
   path = /dev/shm
   browseable = yes
   read only = yes
   guest ok = no
   valid users = digicast
```

6. Restart and enable samba
```
sudo systemctl restart smbd
sudo systemctl enable smbd
```

7. Test your shared folder and access it via Windows by connecting to the same Wi-Fi network chosen in step 2, right-clicking on Network and selecting Map Network Drive. Choose a drive letter, the path is \\digicast\digiball or \\<ip address>\digiball, and then the username (sometimes listed as email) and password. Navigate to the shared Network Drive letter you have chosen. For Mac, open Finder and choose Go -> Connect to Server and enter: ```smb://digicast/digiball``` or ```smb://<ip address>/digiball```. When the DigiBall is working images should appear in this folder. Use these images with OBS for an overlay on a live stream.

8. (Optional) As mentioned it is recommended to use a separate Wi-Fi adapter so that Bluetooth doesn't have to compete with Wi-Fi. Procure and plug in a Wi-Fi dongle into the USB port and use adapters if necessary.

9. Check the interfaces by typing ```nmcli device```. The external USB Wi-Fi dongle is usually ```wlan1```.

10. Check that the Wi-Fi dongle adapter is present on the USB bus with ```lsusb```

11. Check available networks seen by the dongle with ```sudo nmcli device wifi list ifname wlan1```

12. Create a connection with the dongle by typing ```sudo nmcli device wifi connect "YourSSID" password "YourPassword" ifname wlan1```

13. Run ```ifconfig``` and record the IP address for wlan1.

14. Type ```sudo nmcli connection modify "YourSSID" connection.autoconnect no;sudo nmcli device disconnect wlan0``` to disable wlan0. Or use the ```sudo nmtui``` tool to modify the connections directly (and disable wlan0). Note: If YourSSID was the same as an existing connection then the name might automatically change.

15. Save and reboot. (```sudo reboot```). If you are using ssh then you will need to connect to the dongle's new IP address.

16. After reboot type ```nmcli device``` and verify that only the USB Wi-Fi dongle on wlan1 is in use, and that wlan0 is disconnected.

17. Verify that Bluetooth is still working by typing ```hciconfig``` and look for the text UP RUNNING.

18. Finally, enable image generation by typing ```nano ~/digicast/python/bluetooth_le.py``` and changing line 25 to ```self.webserver_image_generation = True```

19. Re-enable the file system overlay. See steps in Enabling Two-Player Mode above.

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

### Writing an Image File to SD Card with Windows

1. If attempting to overwrite an SD Card that was previously used for a Raspberry Pi OS, you will first need to restore the structure of the card into Windows-digestible format. The easiest way to do this is to download the tool SDCardFormatter. A copy of this tool is included in this distribution as windows/SDCardFormatterv5_WinEN.zip. Install the program, make sure to select the first drive letter (bootfs) of the SD Card, and click Quick Format.

2. Optional: Using Windows explorer reformat into exFAT if you desire if you plan on storing files larger than 4GB.

3. Install Win32DiskImager. A copy can be found at windows/win32diskimager-1.0.0-install.exe.

4. Open Win32DiskImager. Under Device, make sure to select the correct SD Card drive letter of the media you want to format. Select your image.img file you made previously.

5. Click Write. The process should take about 9 minutes using USB 3.0.

6. When finished you should see a bunch of messages from Windows complaining about the new SD card formats. Close these and then eject the first drive letter of the SD Card (bootfs).

7. Install the SD card into your Raspberry Pi Zero 2 W and verify that it boots, and that the DigiCast program loads automatically.

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

