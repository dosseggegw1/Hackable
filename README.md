 








sudo apt install -y tcpdump tshark 
https://askubuntu.com/questions/530920/tcpdump-permissions-problem

sudo groupadd pcap
sudo usermod -a -G pcap $USER
sudo chgrp pcap /usr/bin/tcpdump
sudo chmod 750 /usr/bin/tcpdump
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/tcpdump

sudo mkdir /home/pi/pcap
sudo chmod 777 /home/pi/pcap

sudo pip3 install netifaces

sudo apt install dnsmasq
