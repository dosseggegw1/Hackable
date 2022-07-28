# Hackable - Proof of concept

Auteur : Gwendoline Dössegger

Date : 28.07.2022

---

### Installation 

Cette implémentation a été testée sur une Raspberry Pi Zero 2W avec le système d'exploitation Raspberry Pi OS Lite 32bits.  La Pi possède une configuration de base avec SSH et connexion WiFi.

Voici une liste des différentes installations / manipulations a effectuée afin de s'assurer du bon fonctionnement de l'équipement. 

```sh
# Configuration initale
sudo apt update && apt list --upgradable
sudo apt install -y git

# Ajout des modules et drivers



# Récupérer le dépôt /home/pi
git clone DEPOT /home/pi

# On se retrouve donc avec une structure de /home/pi
# - hackable_gadget			# Script pour créer le gadget multifonction
# - hackable.py				# Outil qui orcheste les attaques
# - inject.py
# - pcap					# Destiner à contenir les captures réseaux
#		- README	
# - Stockage_Pi				# Destiner à être copié dans le stockage de masse de la Pi
#		- config.ps1
#		- 
#		- 
#		- 
# - payloads				# Stock les payloads créés
# 		-
# 		-
# 		-
# 		-
# 		-
# 		-
# 		-
# 		-
# 		-

# Création du script du gadget multifonction
sudo cp hackable_gadget /usr/bin/hackable
sudo chmod +x /usr/bin/hackable
```

```sh
# On modifie ensuite le fichier rc.local afin que le script hackable soit lancer à chaque allumage de la Pi. On place le chemin de notre script juste au dessus du exit 0.
sudo nano /etc/rc.local
# [... contenu ...]
/usr/bin/hackable
exit 0		
```

```sh
# Configuration du service DHCP
sudo apt install dnsmasq

echo >> /etc/dnsmasq.conf
echo dhcp-range=10.0.0.10,10.0.0.15,255.255.255.0,12h
```

```sh
# Installations des outils
sudo apt install -y tcpdump tshark --fix-missing
sudo groupadd pcap
sudo usermod -a -G pcap $USER
sudo chgrp pcap /usr/bin/tcpdump
sudo chmod 750 /usr/bin/tcpdump
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/tcpdump
sudo chmod 777 /home/pi/pcap

# Requirements pour l'application Hackable
sudo apt install python3-pip -y
sudo pip3 install netifaces
```

---

### Utilisation de l'application

```sh
# Executer l'application
sudo python3 hackable.py
```

IMG appli

6 options..

----

### Injection de frappes

On utilise le code `inject.py` qui permet de transmettre des frappes. Le code des touches correspond à un clavier suisse version française.

Pour injecter des frappes, nous utilisons le langage Ducky Script dont les syntaxes autorisées sont décrites dans le fichier `payloads/READme.md`.

La Raspberry Pi ou l'équipement qui utilise cette application doit être détecté comme gadget HID et avoir accès à `/dev/hid0`. 

```sh
# Pour uniquement utiliser ce code, utilisez la commande suivante
sudo python3 inject.py [payload_duckyscript]
```

------

### Keylogger

Trois versions ont été créées. Ils sont tous stocké dans le répertoire Stockage_Pi et doivent être copiés dans le stockage de la Pi. 

- 



