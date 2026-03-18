#!/bin/bash

iface=wlan0

#get unique suffix
suffix=$(cat /sys/class/net/$iface/address | awk -F: '{print $4$5$6}')
ssid="DigiCast-$suffix"
echo "Starting hotspot: $ssid"
nmcli connection add type wifi ifname $iface con-name DigiBallHotspot ssid $ssid password digicast autoconnect yes



