#!/usr/bin/env python3
import os
import signal
import subprocess
import sys

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

menu = {
    '1': ['Injection de frappes', {
        '1': ['Linux - Désactive network manager & force réseau ethernet', 'payloads/linux-network.dd'],
        '2': ['Kubuntu - Récupère les mots de passe de Chrome', 'payloads/kubuntu-chrome-password.dd'],
        '3': ['Kubuntu - Vérifie l\'injecteur de frappes opérationnel', 'payloads/kubuntu-test.dd'],
        '4': ['Windows - Désactive scan Windows Defender de la Pi', 'payloads/windows-defender.dd'],
        '5': ['Windows - Récupère les mots de passe de Chrome', 'payloads/windows-chrome-password.dd'],
        '6': ['Windows - Vérifie l\'injecteur de frappes opérationnel', 'payloads/windows-test.dd'],
        '7': ['Executer son propre payload', 'payloads/'],
    }],
    '2': ['Keylogger [Windows|Linux]', {
        '1': ['Windows Keylogger sans mail', 'keyloggers/keylogger-windows.dd'],
        '2': ['Kubuntu Keylogger sans mail', 'keyloggers/keylogger-linux.dd'],
        '3': ['Kubuntu Keylogger avec mail', 'keyloggers/keylogger-linux-smtp.dd'],
    }],
    '3': ['MITM Ethernet - Écoute du réseau', {
        '1': ['Tshark - Ecoute l\'interface usb0', ['sudo','tshark', '-i', 'usb0', '-w', '/home/pi/pcap/tshark.pcap']],
        '2': ['Tcpdump - Ecoute de l\'intrface usb0', ['sudo', 'tcpdump', '-i', 'usb0', '-tttt', '-w', 'pcap/tcpdump.pcap']],
        '3': ['Tcpdump - Ecoute de l\'intrface usb0 filtrer port 80', ['sudo', 'tcpdump', '-i', 'usb0', '-tttt', '-w', 'pcap/tcpdump_80.pcap', 'port', '443']],
    }],
    '4': ['MITM USB - Attaque sur un smartphone', {
        '1': ['Injection de frappes', 'sudo python3 inject.py'],
        '2': ['Récupération de vidéo via un mail', 'sudo python3 inject.py android-mail.dd'],
    }],
}


# Nettoie le terminal et affiche la banière
def clear_console():
    os.system('clear')
    print(banner)

# Injection de frappes sur la machine hôte
def injection(dico):
    clear_console()
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

        # Permet d'exécuter le payload de son choix
        elif choice == '7':
            print("Le payload doit être stocké dans le répertoire /home/pi/payloads/")
            choice = input(f'\nQuelle option voulez-vous lancer [ex : payload.dd]? ')
            path_file = 'payloads/' + choice
            subprocess.Popen(['sudo','python3','inject.py',path_file], start_new_session=True)
            clear_console()
            print(f'Payload : {choice} exécuté !\n')
            return


        # Execute des payloads deja référencés
        else:
            subprocess.Popen(['sudo','python3','inject.py',dico[choice][1]], start_new_session=True)
            clear_console()
            print(f'Payload : {dico[choice][0]} exécuté !\n')
            return

# Permet d'exécuter un Keylogger sur la machine hôte via l'injecteur de frappes
# Compatible avec Windows et Linux.
# Attention, les keyloggers doivent être présents dans le stockage de masse
def keylogger(dico):
    clear_console()
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
            path_file = input(f'\nOù voulez-vous stocker le fichier ?')
            print(path_file)

            file = path_payloads + dico[choice][1]
            # sudo python3 inject.py file
            # Saisie utilisateur

            clear_console()
            print(f'Keylogger {dico[choice][0]} exécuté !\n')
            return

# Scan le réseau et plus précisément l'interface usb0
def mitm_ethernet(dico):
    clear_console()
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

        # Execute l'attaque
        else:
            # Saisie utilisateur
            run_time = int(input("\nCombien de temps voulez-vous scanner le réseau ? "))

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


def mitm_usb(dico):
    clear_console()
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

        # Execute l'attaque
        else:
            # dico[choice][1]

            clear_console()
            print(f'Scan {dico[choice][0]} exécuté !\n')
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
