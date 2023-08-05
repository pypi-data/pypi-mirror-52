#!/bin/sh
file=/etc/hostname
file2=/etc/hosts
host=$1
sed -i "1s/.*/$host/" $file
sed -i 's/127.0.1.1.*/127.0.1.1       '$host'/' $file2
