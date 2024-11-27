from bleak import BleakScanner
import asyncio
import struct
from math import *
class BLE_async():

    def __init__(self):
        self.test = True
        self._devices = None
        self._done = True
        self._last_shot_number = -1
        self._digiball_mac_addresses = [None, None]
        self._digicue_mac_addresses = [None, None]

    def get_test_data(self):
        #For testing only

        data = {}
        data["RSSI"] = -70
        data["MAC Address"] = "mac1"
        data["Charging"] = 0
        data["Gyro Clipping"] = False
        data["Motionless"] = 0
        data["Shot Number"] = 0
        data["Tip Percent"] = 25
        data["Speed KMPH"] = 5
        data["Spin RPS"] = 3
        data["Tip Angle"] = 45

        self._digiball_mac_addresses[0] = data["MAC Address"]

        digiball_data = [data,None]
        digicue_data = [data,None]

        return digiball_data, digicue_data





    async def _scan(self):
        self._devices = await BleakScanner.discover(2.0, return_adv=True)

    def _digiball_parser(self, devices):

        player_data = [None, None]

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
                        if self._digiball_mac_addresses[0] is None and rssi>rssi_range:
                            self._digiball_mac_addresses[0] = mac_address
                        elif self._digiball_mac_addresses[1] is None and rssi>rssi_range and mac_address!=self._digiball_mac_addresses[0]:
                            self._digiball_mac_addresses[1] = mac_address

                        if mac_address in self._digiball_mac_addresses:

                            if mac_address == self._digiball_mac_addresses[0]:
                                player = 1
                            else:
                                player = 2

                            data_ready = (int(mdata[17]) >> 6) == 1
                            shot_number = int(mdata[6]) & 0x3F

                            if data_ready:
                                data = {}
                                data["RSSI"] = rssi
                                data["MAC Address"] = mac_address

                                #Parse digiball data here
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

                                #Post data
                                player_data[player-1] = data
        return player_data
    def _digicue_parser(self, devices):

        player_data = [None, None]

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
                        if self._digicue_mac_addresses[0] is None and rssi>rssi_range:
                            self._digicue_mac_addresses[0] = mac_address
                        elif self._digicue_mac_addresses[1] is None and rssi>rssi_range and mac_address!=self._digicue_mac_addresses[0]:
                            self._digicue_mac_addresses[1] = mac_address

                        if mac_address in self._digicue_mac_addresses:

                            if mac_address == self._digicue_mac_addresses[0]:
                                player = 1
                            else:
                                player = 2

                            data_ready = (int(mdata[17]) >> 6) == 1
                            shot_number = int(mdata[6]) & 0x3F

                            if data_ready:
                                data = {}
                                data["RSSI"] = rssi
                                data["MAC Address"] = mac_address

                                #Parse digicue data here

                                #Post data
                                player_data[player-1] = data
        return player_data


    def async_task(self,q):
        try:
            asyncio.run(self._scan())
            digiball_data = self._digiball_parser(self._devices)
            digicue_data = self._digicue_parser(self._devices)
            q.put((digiball_data, digicue_data))
        except:
            pass

