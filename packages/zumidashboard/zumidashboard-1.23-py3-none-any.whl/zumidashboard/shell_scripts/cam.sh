#!/bin/sh
file=/boot/config.txt
if grep -q 'start_x' $file; then
sed -i 's/start_x=.*/start_x=1''/' $file
else
sed -i '1a start_x=1' $file
fi
if grep -q 'dtparam=i2c_arm' $file; then
sed -i 's/dtparam=i2c_arm=.*/dtparam=i2c_arm=on''/' $file
else
sed -i '$ a dtparam=i2c_arm=on' $file
fi
#sed -i 's#sudo /home/pi/cam.sh# #g' /etc/rc.local
