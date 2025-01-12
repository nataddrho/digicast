from bleak import BleakScanner
import asyncio
import struct
from math import *
class BLE_async():

    def __init__(self):
        self.test = False #Turn on to test graphical display
        self._done = True
        self._last_shot_number = -1
        self._digiball_mac_addresses = [None, None]
        self._digicue_mac_addresses = [None, None]
        self._digiball_player_data = [None, None]
        self._digicue_player_data = [None, None]
        self._new_device = False

    def check_for_new_device(self): # Returns true if a new device was found. Clear screen if true
        new = self._new_device
        self._new_device = False
        return new

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
        data["Ball Diameter"] = 2.25
        data["Ball Color"] = "White"
        data["Tip Diameter"] = 11.8 / 25.4
        data["Tip Curvature"] = 0.358
        data["Straightness"] = 0.9
        data["Straightness Text"] = "0.9"
        data["Straightness Threshold"] = 0.2
        data["Straightness Enabled"] = True
        data["Straightness Angle"] = 45
        data["Finish"] = 0.1
        data["Finish Text"] = "0.1"
        data["Finish Threshold"] = 0.3
        data["Finish Enabled"] = True
        data["Tip Steer"] = 0.2
        data["Tip Steer Text"] = "0.2"
        data["Tip Steer Threshold"] = 0.3
        data["Tip Steer Enabled"] = True
        data["Follow Through"] = 0.3
        data["Follow Through Text"] = "0.3"
        data["Follow Through Threshold"] = 0.3
        data["Follow Through Enabled"] = True
        data["Jab"] = 0.4
        data["Jab Text"] = "0.4"
        data["Jab Threshold"] = 0.3
        data["Jab Enabled"] = True
        data["Backstroke Pause"] = 0.5
        data["Backstroke Pause Text"] = "0.5"
        data["Backstroke Pause Threshold"] = 0.3
        data["Backstroke Pause Enabled"] = True
        data["Shot Interval"] = 0.6
        data["Shot Interval Text"] = "0.6"
        data["Shot Interval Threshold"] = 0.3
        data["Shot Interval Enabled"] = True

        self._digiball_mac_addresses[0] = data["MAC Address"]

        digiball_data = [data,None]
        digicue_data = [None,None]

        return digiball_data, digicue_data

    def _digiball_parser(self, device, advertising_data):
        mac_address = device.address
        d = advertising_data
        rssi = d.rssi
        manuf = d.manufacturer_data
        for manuf_id in manuf:

            if manuf_id == 0x03DE: #NRLLC

                mdata = manuf[manuf_id]
                device_type = int(mdata[3]&0xF)

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



                            ball_types = ((2.250, "White", 0.465, 0.358),  # Pool
                                          (2.438, "White", 0.465, 0.358),  # Carom
                                          (2.438, "Yellow", 0.465, 0.358),  # Carom yellow
                                          (2.063, "White", 0.354, 0.250),  # Snooker
                                          (2.000, "White", 0.315, 0.250),  # English pool
                                          (2.688, "White", 0.492, 0.375))  # Russian pyramid

                            ball_type = (mdata[3] >> 4) & 0xF
                            if ball_type>(len(ball_types)-1):
                                ball_type = 0

                            properties = ball_types[ball_type]

                            data["Ball Diameter"] = properties[0]
                            data["Ball Color"] = properties[1]
                            data["Tip Diameter"] = properties[2]
                            data["Tip Curvature"] = properties[3]

                            #Post data
                            if self._digiball_player_data[player-1] is None:
                                self._new_device = True
                            self._digiball_player_data[player-1] = data
                            return True

        return False

    def _digicue_parser(self, device, advertising_data):
        mac_address = device.address
        d = advertising_data
        rssi = d.rssi
        manuf = d.manufacturer_data
        for manuf_id in manuf:

            if manuf_id == 0xDE03: #NRLLC reversed

                mdata = manuf[manuf_id]

                if len(mdata)==17: #DigiCue data is 17 bytes in length

                    # Save device as target if brought close to receiver
                    rssi_range = -65
                    if self._digicue_mac_addresses[0] is None and rssi>rssi_range:
                        self._digicue_mac_addresses[0] = mac_address
                    elif self._digicue_mac_addresses[1] is None and rssi>rssi_range and mac_address!=self._digicue_mac_addresses[0]:
                        self._digicue_mac_addresses[1] = mac_address

                    if mac_address in self._digicue_mac_addresses:

                        if mac_address == self._digicue_mac_addresses[0]:
                            player = 1
                        else:
                            player = 2

                        config = mdata[1]
                        aconf0 = mdata[2]
                        aconf1 = mdata[3]
                        aconf2 = mdata[4]
                        aconf3 = mdata[5]
                        data_type = (config>>3)&3

                        if data_type<=1:

                            alert0 = mdata[6]
                            alert1 = mdata[7]
                            shot_timer = mdata[8]
                            pause_time = mdata[9]
                            follow_thru = mdata[10]
                            jab_mag = mdata[11]
                            impact_angle = mdata[12] * 180 / 128.0
                            impact_mag = mdata[13] / 255.0
                            freeze_ang = mdata[14] * 180 / 128.0
                            freeze_time = mdata[15]
                            freeze_mag = alert1 >> 1

                            score_finish = (freeze_time + 48) * 0.012
                            score_backstroke = pause_time * 0.012
                            tmp = jab_mag;
                            if (tmp > 125):
                                tmp = 125
                            score_jab = (125 - tmp) / 12.5
                            score_follow = follow_thru - 1
                            if score_follow<0:
                                score_follow = 0
                            alert_steer_right = sin(impact_angle * pi / 180) < 0

                            steering_dir = alert1&1==1

                            tmp = impact_mag * 255
                            if tmp > 50:
                                tmp = 50
                            score_straightness = (50-tmp) / 5.0
                            score_steering = score_straightness * abs(cos(impact_angle * pi / 180))
                            score_interval = shot_timer / 255;

                            straightness_t = [0.893, 0.785, 0.571, 0.25]
                            steering_t = straightness_t
                            follow_t = [.4, .7, .9, 1]
                            jab_t = [.8, .6, .4, .2]
                            backstroke_t = [.1, .2, .5, 1]
                            interval_t = [0.0382, 0.0612, 0.0919, 0.114]
                            finish_t = [1/3, 1.5/3, 2/3, 2.5/3]

                            data = {}
                            data["RSSI"] = rssi
                            data["MAC Address"] = mac_address

                            #Parse digicue data here
                            data["Straightness"] = score_straightness/10
                            data["Straightness Text"] = "%.1f"%score_straightness
                            data["Straightness Threshold"] = straightness_t[(aconf2>>2)&3]
                            data["Straightness Enabled"] = (aconf0>>5)&1==1
                            data["Straightness Angle"] = impact_angle
                            data["Finish"] = score_finish/3
                            data["Finish Text"] = "%.1fs"%(score_finish)
                            data["Finish Threshold"] = finish_t[(aconf2>>6)&3]
                            data["Finish Enabled"] = (aconf0>>7)&1==1
                            data["Tip Steer"] = score_steering/10
                            data["Tip Steer Text"] = "%.1f"%score_steering
                            data["Tip Steer Threshold"] = data["Straightness Threshold"] #steering_t[aconf2&3]
                            data["Tip Steer Enabled"] = (aconf0>>4)&1==1
                            data["Follow Through"] = score_follow/10
                            data["Follow Through Text"] = "%.1f"%score_follow
                            data["Follow Through Threshold"] = follow_t[(aconf1>>6)&3]
                            data["Follow Through Enabled"] = (aconf0>>3)&1==1
                            data["Jab"] = score_jab/10
                            data["Jab Text"] = "%.1f"%score_jab
                            data["Jab Threshold"] = jab_t[(aconf1>>4)&3]
                            data["Jab Enabled"] = (aconf0>>2)&1==1
                            data["Backstroke Pause"] = score_backstroke
                            data["Backstroke Pause Text"] = "%.1fs"%score_backstroke
                            data["Backstroke Pause Threshold"] = backstroke_t[(aconf1>>2)&3]
                            data["Backstroke Pause Enabled"] = (aconf0>>1)&1==1
                            data["Shot Interval"] = score_interval
                            data["Shot Interval Text"] = "%is"%(shot_timer * 0.512)
                            data["Shot Interval Threshold"] = interval_t[aconf1&3]
                            data["Shot Interval Enabled"] = aconf0&1==1

                            #Post data
                            if self._digicue_player_data[player-1] is None:
                                self._new_device = True
                            self._digicue_player_data[player-1] = data
                            return True

        return False

    async def _scan(self, q):
        stop_event = asyncio.Event()

        def callback(device, advertising_data):
            #Calls on every advertisement received
            db = self._digiball_parser(device, advertising_data)
            dc = self._digicue_parser(device, advertising_data)
            if (db or dc):
                #Post everytime a packet is successfully parsed
                q.put((self._digiball_player_data, self._digicue_player_data))

        async with BleakScanner(callback) as scanner:
            # Important! Wait for an event to trigger stop, otherwise scanner
            # will stop immediately.
            await stop_event.wait()


    def async_task(self, q):
        asyncio.run(self._scan(q))


