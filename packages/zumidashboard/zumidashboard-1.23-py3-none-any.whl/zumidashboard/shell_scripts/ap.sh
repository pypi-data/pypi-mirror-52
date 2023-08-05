#!/bin/sh
file=/etc/dhcpcd.conf
if !(grep -q 'interface wlan0' $file);then
sed -i '$ a interface wlan0' $file
sed -i '$ a static ip_address=192.168.0.10/24' $file
sed -i '$ a nohook wpa_supplicant' $file
fi
sudo service dhcpcd restart
sudo systemctl start hostapd
