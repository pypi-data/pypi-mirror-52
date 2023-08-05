#!/bin/sh
file=/etc/dhcpcd.conf
sudo systemctl stop hostapd
while true; do
if grep -q 'interface wlan0' $file; then
sed -i '/interface wlan0/d' $file
sed -i 's#static ip_address=192.168.0.10/24# #g' $file
sed -i '/nohook wpa_supplicant/d' $file
else
break
fi
done
sudo systemctl restart dnsmasq
sudo service dhcpcd restart
sleep 15

ssid=$(iwgetid | grep ESSID)
v=$(echo $ssid | cut -d'"' -f 2)

if test -z "$v"; then
sudo /home/pi/Flask-AP/ap.sh
fi

