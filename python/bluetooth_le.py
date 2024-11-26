from bleak import BleakScanner
import asyncio
import struct
from math import *
class BLE_async():

    def __init__(self):
        self._devices = None
        self._done = True
        self._last_shot_number = -1
        self.digiball_mac_addresses = [None, None]
        self.digicue_mac_addresses = [None, None]

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
                        if self.digiball_mac_addresses[0] is None and rssi>rssi_range:
                            self.digiball_mac_addresses[0] = mac_address
                        elif self.digiball_mac_addresses[1] is None and rssi>rssi_range and mac_address!=self.digiball_mac_addresses[0]:
                            self.digiball_mac_addresses[1] = mac_address

                        if mac_address in self.digiball_mac_addresses:

                            if mac_address == self.digiball_mac_addresses[0]:
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
                        if self.digicue_mac_addresses[0] is None and rssi>rssi_range:
                            self.digicue_mac_addresses[0] = mac_address
                        elif self.digicue_mac_addresses[1] is None and rssi>rssi_range and mac_address!=self.digicue_mac_addresses[0]:
                            self.digicue_mac_addresses[1] = mac_address

                        if mac_address in self.digicue_mac_addresses:

                            if mac_address == self.digicue_mac_addresses[0]:
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

