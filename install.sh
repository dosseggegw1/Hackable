#!/bin/bash

# Hackable install script
# Author : Gwendoline Dössegger
# Date   : 26.07.2022
# Info   : 
# - install.sh you should only be run once.
# - this projet is work in progress (may contains error)
#
# Based on RoganDawes's script
# source : https://github.com/RoganDawes/P4wnP1/blob/master/install.sh

wdir=/home/pi

# check Internet conectivity
echo "Testing Internet connection and name resolution..."
if [ "$(curl -s http://www.msftncsi.com/ncsi.txt)" != "Microsoft NCSI" ]; then 
        echo "...[Error] No Internet connection or name resolution doesn't work! Exiting..."
        exit
fi
echo "...[pass] Internet connection works"

# Configure the Pi zero 2W
sudo apt update -y && apt list --upgradable
sudo apt install python3-pip dnsmasq git -y
 
 
sudo bash -c "echo  >> /etc/resolv.conf"

 
 
# Add network configuration
sudo bash -c "echo nameserver 8.8.8.8 >> /etc/resolv.conf"

sudo bash -c "echo nameserver 8.8.8.8 >> /etc/resolv.conf"
 
# Install tools
echo "Installing tools for Hackable"
sudo apt install -y tcpdump tshark --fix-missing
sudo groupadd pcap
sudo usermod -a -G pcap $USER
sudo chgrp pcap /usr/bin/tcpdump
sudo chmod 750 /usr/bin/tcpdump
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/tcpdump


# Install Hackable application
DL github
sudo pip3 install netifaces
