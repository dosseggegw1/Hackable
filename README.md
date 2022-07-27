 





sudo apt update && apt list --upgradable

sudo apt install -y tcpdump tshark git --fix-missing
https://askubuntu.com/questions/530920/tcpdump-permissions-problem

sudo groupadd pcap
sudo usermod -a -G pcap $USER
sudo chgrp pcap /usr/bin/tcpdump
sudo chmod 750 /usr/bin/tcpdump
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/tcpdump

COPIER LE GITHUB

sudo mkdir /home/pi/pcap
sudo chmod 777 /home/pi/pcap

sudo apt install python3-pip -y

sudo pip3 install netifaces



GADGET

sudo apt install dnsmasq

sudo nano /etc/dnsmasq.conf -> avec config IP

sudo systemctl start dnsmasq

sudo systemctl enable dnsmasq

sudo service dnsmasq restart
