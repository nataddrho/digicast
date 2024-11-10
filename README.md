

# digiball-pi
A light-weight Python-based application for Raspberry Pi Zero 2 W (or any other platform that has BLE hardware and can run Python). The program displays information from one or two DigiBalls in real time. This is BLE straight to HDMI solution.

### Requirements:

Raspberry Pi Zero 2 W
Micro-SD card (16 GB or greater)
PC with a micro-SD card reader or USB reader
Micro HDMI to HDMI cable
5VDC Power Adapter (greater than 1 amp)

### Installation:

1. Download the Raspberry Pi Imager software (v1.8.5 used at the time of writing this).

2. Choose Raspberry Pi Zero 2 W for the device.

3. Choose Raspberry Pi OS (64-bit) (recommended) for the operating system.

4. Choose your micro-SD card as the storage solution.

5. Optional: Set up user name and password, and SSH.

6. Build image on micro-SD card

7. Install the card into the Zero 2, plug a mouse and keyboard through a USB hub into the micro-USB port, and power on. Or connect remotely with SSH if you know the IP address already.

8. Wait for the system to boot into the Desktop. Navigate to Raspberry Pi Configuration and change Boot to CLI. Save and restart. Alternatively, you can open a terminal and perform the same operation by using the ```raspi-config``` command. Reboot by typing ```sudo shutdown -r now```

9. Run an update by running ```sudo apt update```

10. Install the BLE library Bleak by running ```sudo apt install python3-bleak```

11. Clone the digiball-pi repository with ```git clone https://github.com/nataddrho/digiball-pi.git```

12. Create an automatic launch script. ```sudo nano /etc/rc/local``` Before ```exit 0``` at the bottom of the file, add

```
cd /home/username/digiball-pi/python
python main.py pool
```

Replace "pool" with "snooker" or "carom" depending on the type of DigiBall you own.

13. Put the file system into read-only mode by creating an overlay. This protects from corruption caused by turning off the power of the Raspberry Pi abruptly (which is what we want to do). Run ```sudo raspi-config```, navigate to Performance Options, Overlay File System and press enter. Select Yes when prompted to enable the overlay file system. Select Yes when prompted to write-protect the boot partition.

14. Reboot the system.

15. The DigiBall application should start automatically on every power up.


### How to Use:

![alt text](https://github.com/nataddrho/digiball-pi/python/oneplayer.jpg?raw=true)

