#!/usr/bin/python

"""
# Base code : https://stackoverflow.com/questions/49887540/improve-python-code
# Comparaison disposition : https://www.sbsupply.eu/blog/what-is-the-difference-between-qwerty-qwerty-nl-azerty-and-qwertz
# Code selon : https://github.com/tejado/Authorizer/blob/master/authorizer/src/main/java/net/tjado/authorizer/UsbHidKbd_fr_CH.java

HID Keyboard Mapper
By: Gwendoline Dössegger
Date: 2022


"""

from time import sleep
import sys

#Variables
NULL_CHAR = chr(0)

#Dictionary
# 0x00 0x00 0x?? 0x00 0x00 0x00 0x00 0x00 | valeur de la touche par défaut
keys_none = {
'a': '4', 'b': '5', 'c': '6', 'd': '7', 'e': '8', 'f': '9', 'g': '10', 'h': '11', 'i': '12', 'j': '13', 'k': '14',
'l': '15', 'm': '16', 'n': '17', 'o': '18', 'p': '19', 'q': '20', 'r': '21', 's': '22', 't': '23', 'u': '24', 'v': '25',
'w': '26', 'x': '27', 'y': '29', 'z': '28', '1':'30', '2':'31', '3':'32', '4':'33', '5':'34', '6':'35', '7':'36',
'8':'37', '9':'38', '0':'39', '\'':'45', '§':'53', 'è':'47', '¨':'48', '$':'50', 'é':'51', 'à':'52', ',':'54',
'.':'55', '-':'56', '<':'100', ' ':'44', '   ':'43',
}

# 0x02 0x00 0x?? 0x00 0x00 0x00 0x00 0x00 | valeur de la touche si shift cliqué
keys_maj = {
'A': '4', 'B': '5', 'C': '6', 'D': '7', 'E': '8', 'F': '9', 'G': '10', 'H': '11', 'I': '12', 'J': '13', 'K': '14',
'L': '15', 'M': '16', 'N': '17', 'O': '18', 'P': '19', 'Q': '20', 'R': '21', 'S': '22', 'T': '23', 'U': '24', 'V': '25',
'W': '26', 'X': '27', 'Y': '29', 'Z': '28', '+':'30', '"':'31', '*':'32', 'ç':'33', '%':'34', '&':'35', '/':'36',
'(':'37', ')':'38', '=':'39', '?':'45', '°':'53', 'ü':'47', '!':'48', '£':'50', 'ö':'51', 'ä':'52', ';':'54',
':':'55', '_':'56', '>':'100',
}

# 0x40 0x00 0x?? 0x00 0x00 0x00 0x00 0x00 | valeur de la touche si alt gr cliqué
keys_alt = {
'¦':'30', '@':'31', '#':'32', '¼':'33', '½':'34', '¬':'35', '|':'36', '¢':'37', ']':'38', '}':'39', '€':'8', '[':'47',
']':'48', '}':'50', '{':'52', '\\':'100',
}

keys_special = { # Enchainement de touche spécial
'´':'write_report(chr(64)+NULL_CHAR+chr(45)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)\nwrite_report(chr(64)+NULL_CHAR+chr(45)+NULL_CHAR*5)\n',  # AFFICHE ´´ au lieu de ´
'~':'write_report(chr(64)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)\nwrite_report(NULL_CHAR*2 +chr(41)+NULL_CHAR*5)', # souci de ~+espace au lieu de ~
'^':'write_report(NULL_CHAR*2 +chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)\nwrite_report(NULL_CHAR*2 +chr(41)+NULL_CHAR*5)', # SEE APRES ^+espace au lieu de ^
'`':'write_report(chr(2)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)\nwrite_report(NULL_CHAR*2 +chr(41)+NULL_CHAR*5)', # SEE APRES `+espace au lieu de `

#ïÏíÍìÌîÎĩĨ
'ï':'write_report(NULL_CHAR*2 +chr(48)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(12)+NULL_CHAR*5)',
'Ï':'write_report(NULL_CHAR*2 +chr(48)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(12)+NULL_CHAR*5)',
'í':'write_report(chr(64)+NULL_CHAR+chr(45)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(12)+NULL_CHAR*5)',
'Í':'write_report(chr(64)+NULL_CHAR+chr(45)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(12)+NULL_CHAR*5)',
'ì':'write_report(chr(2)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(12)+NULL_CHAR*5)',
'Ì':'write_report(chr(2)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(12)+NULL_CHAR*5)',
'î':'write_report(NULL_CHAR*2 +chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(12)+NULL_CHAR*5)',
'Î':'write_report(NULL_CHAR*2 +chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(12)+NULL_CHAR*5)',
'ĩ':'write_report(chr(64)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(12)+NULL_CHAR*5)',      # ĩ = ~i
'Ĩ':'write_report(chr(64)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(12)+NULL_CHAR*5)',  # Ĩ = ~I

#ëËéÉèÈêÊẽẼ
'ë':'write_report(NULL_CHAR*2 +chr(48)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(8)+NULL_CHAR*5)',
'Ë':'write_report(NULL_CHAR*2 +chr(48)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(8)+NULL_CHAR*5)',
'É':'write_report(chr(64)+NULL_CHAR+chr(45)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(8)+NULL_CHAR*5)',
'È':'write_report(chr(2)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(8)+NULL_CHAR*5)',
'ê':'write_report(NULL_CHAR*2 +chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(8)+NULL_CHAR*5)',
'Ê':'write_report(NULL_CHAR*2 +chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(8)+NULL_CHAR*5)',
'ẽ':'write_report(chr(64)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(8)+NULL_CHAR*5)',       # ẽ = ~e
'Ẽ':'write_report(chr(64)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(8)+NULL_CHAR*5)',   # Ẽ = ~E

#öÖóÓòÒôÔõÕ
'Ö':'write_report(NULL_CHAR*2 +chr(48)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(18)+NULL_CHAR*5)',
'ó':'write_report(chr(64)+NULL_CHAR+chr(45)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(18)+NULL_CHAR*5)',
'Ó':'write_report(chr(64)+NULL_CHAR+chr(45)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(18)+NULL_CHAR*5)',
'ò':'write_report(chr(2)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(18)+NULL_CHAR*5)',
'Ò':'write_report(chr(2)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(18)+NULL_CHAR*5)',
'ô':'write_report(NULL_CHAR*2 +chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(18)+NULL_CHAR*5)',
'Ô':'write_report(NULL_CHAR*2 +chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(18)+NULL_CHAR*5)',
'õ':'write_report(chr(64)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(18)+NULL_CHAR*5)',
'Õ':'write_report(chr(64)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(18)+NULL_CHAR*5)',

#äÄáÁàÀâÂãÃ
'Ä':'write_report(NULL_CHAR*2 +chr(48)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(4)+NULL_CHAR*5)',
'á':'write_report(chr(64)+NULL_CHAR+chr(45)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(4)+NULL_CHAR*5)',
'Á':'write_report(chr(64)+NULL_CHAR+chr(45)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(4)+NULL_CHAR*5)',
'à':'write_report(chr(2)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(4)+NULL_CHAR*5)',
'À':'write_report(chr(2)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(4)+NULL_CHAR*5)',
'â':'write_report(NULL_CHAR*2 +chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(4)+NULL_CHAR*5)',
'Â':'write_report(NULL_CHAR*2 +chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(4)+NULL_CHAR*5)',
'ã':'write_report(chr(64)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(4)+NULL_CHAR*5)',
'Ã':'write_report(chr(64)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(4)+NULL_CHAR*5)',

#üÜúÚùÙûÛũŨ
'Ü':'write_report(NULL_CHAR*2 +chr(48)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(24)+NULL_CHAR*5)',
'ú':'write_report(chr(64)+NULL_CHAR+chr(45)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(24)+NULL_CHAR*5)',
'Ú':'write_report(chr(64)+NULL_CHAR+chr(45)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(24)+NULL_CHAR*5)',
'ù':'write_report(chr(2)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(24)+NULL_CHAR*5)',
'Ù':'write_report(chr(2)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(24)+NULL_CHAR*5)',
'û':'write_report(NULL_CHAR*2 +chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(24)+NULL_CHAR*5)',
'Û':'write_report(NULL_CHAR*2 +chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(24)+NULL_CHAR*5)',
'ũ':'write_report(chr(64)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(24)+NULL_CHAR*5)',      # ~u
'Ũ':'write_report(chr(64)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(24)+NULL_CHAR*5)',  # ~U

#ńŃǹǸñÑ
'ń':'write_report(chr(64)+NULL_CHAR+chr(45)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(17)+NULL_CHAR*5)',      # ´n
'Ń':'write_report(chr(64)+NULL_CHAR+chr(45)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(17)+NULL_CHAR*5)',  # ´N
'ǹ':'write_report(chr(2)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(17)+NULL_CHAR*5)',       # `n
'ǹ':'write_report(chr(2)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(17)+NULL_CHAR*5)',   # `N
'ñ':'write_report(chr(64)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR*2 +chr(17)+NULL_CHAR*5)',
'Ñ':'write_report(chr(64)+NULL_CHAR+chr(46)+NULL_CHAR*5)\nwrite_report(chr(2)+NULL_CHAR+chr(17)+NULL_CHAR*5)',
}


keys_cmd = {
'NONE'  : 'write_report(NULL_CHAR*2',
'LCTRL' : 'write_report(chr(1)+NULL_CHAR',
'LSHIFT': 'write_report(chr(2)+NULL_CHAR',
'LALT'  : 'write_report(chr(4)+NULL_CHAR',
'LMETA' : 'write_report(chr(8)+NULL_CHAR',
'RCTRL' : 'write_report(chr(16)+NULL_CHAR',
'RSHIFT': 'write_report(chr(32)+NULL_CHAR',
'RALT'  : 'write_report(chr(64)+NULL_CHAR',
'RMETA' : 'write_report(chr(128)+NULL_CHAR',
}

# 0x00 0x00 0x?? 0x00 0x00 0x00 0x00 0x00 | valeur de la touche par défaut
keys_mod = {
'F1' :  '58',
'F2' :  '59',
'F4' :  '60',
'F4' :  '61',
'F5' :  '62',
'F6' :  '63',
'F7' :  '64',
'F8' :  '65',
'F9' :  '66',
'F10' : '67',
'F11' : '68',
'F12' : '69',
'SCROLL_LOCK' : '71',
'PAUSE' : '72',
'INSERT' : '73',
'HOME' : '74',
'PAGE_UP' : '75',
'DELETE' : '76',
'END' : '77',
'PAGE_DOWN' : '78',
'ARROW_R' : '79',
'ARROW_L' : '80',
'ARROW_D' : '81',
'ARROW_U' : '82',
'APP' : '101',
'ESC' : '41',
'BACKSPACE' : '42',
'TAB':'43',
'CAPSLOCK':'57',
'PRINT':'70',
'ENTER':'40',
'ESPACE':'44',
'SPACE':'44',
'RETURN':'40',
}

# Fonction qui transmet les HID codes à la victime (représente le HID keyboard)
def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

# Fonction
def sendString(letter):
    if letter in keys_none:
        return keys_cmd['NONE']+'+chr('+keys_none[letter]+')+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)'
    elif letter in keys_maj:
        return keys_cmd['LSHIFT']+'+chr('+keys_maj[letter]+')+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)'
    elif letter in keys_alt:
        return keys_cmd['RALT']+'+chr('+keys_alt[letter]+')+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)'
    elif letter in keys_special:
        return keys_special[letter]

defaultDelay = 0

# Quand CTRL, ALT,
def get_str(cmd,key):
    if not key:
        return keys_cmd[cmd] + '+NULL_CHAR*6)\nwrite_report(NULL_CHAR * 8)'

    elif key in keys_none:
        return keys_cmd[cmd]+'+chr('+keys_none[key]+')+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)'

    elif key in keys_maj:
        return keys_cmd[cmd]+'+chr('+keys_maj[key]+')+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)'

    elif key in keys_alt:
        return keys_cmd[cmd]+'+chr('+keys_alt[key]+')+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)'

    elif key in keys_mod:
        return keys_cmd[cmd]+'+chr('+keys_mod[key]+')+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)'

    elif key in keys_special:
        return keys_special[key]



translated_list = []

def parseLine(line):
    global defaultDelay

    # WINDOWS + [..]
    if line == 'WINDOWS':
        translated_list.append(keys_cmd['LMETA'] + '+chr(21)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)')

    # GUI + []
    elif line.startswith('GUI'):
        str = get_str('LMETA', line[4:])
        translated_list.append(str)

    # CTRL + []
    elif line.startswith('CTRL'):
        str = get_str('LCTRL', line[5:])
        translated_list.append(str)

    # ALT Left + [END, ESC, ESCAPE, F1…F12, Single Char, SPACE, TAB]
    elif line.startswith('ALT'):
        str = get_str('LALT', line[4:])
        translated_list.append(str)

    # ALT Left + [END, ESC, ESCAPE, F1…F12, Single Char, SPACE, TAB]
    elif line.startswith('SHIFT'):
        str = get_str('LSHIFT', line[6:])
        translated_list.append(str)

    elif line == 'MENU': # SHIFT + F10 -> vaut clic droit sur windows
        translated_list.append(keys_cmd['LSHIFT']+'+chr('+keys_mod['f10']+')+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)')

    # Touche de commandes
    elif line == 'TAB' or line == 'ENTER' or line == 'RETURN' or line == 'ESC' or line == 'BACKSPACE' or \
         line == 'CAPSLOCK' or line == 'PRINT' or line == 'SCROLL_LOCK' or line == 'PAUSE' or line == 'INSERT' or \
         line == 'HOME' or line == 'PAGE_UP' or line == 'DELETE' or line == 'END' or line == 'PAGE_DOWN' or \
         line == 'APP' or line == 'ARROW_R' or line == 'ARROW_L' or line == 'ARROW_D' or line == 'ARROW_U' or line == 'ESPACE':
        translated_list.append(keys_cmd['NONE'] +'+chr('+keys_mod[line]+')+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)')

    # STRING + [ a…z A…Z 0…9 !…) `~+=_-“‘;:<,>.?[{]}/|!@#$%^&*() ]
    elif line.startswith('STRING'):  # part du principe que sinon c'est STRING ...
        for letter in line[7:]:
            translated_list.append(sendString(letter))

if __name__ == '__main__':
    try:
        file_name = "payload.dd"
        if len(sys.argv) > 1 :
            file_name = sys.argv[1]

        with open(file_name,"r",encoding='utf-8') as f:
            lines = f.read().splitlines()
            for line in lines:
                if line.startswith('REM'):
                    pass

                elif line.startswith("DEFAULTDELAY"):
                    defaultDelay = int(line[13:]) * 10

                elif line.startswith('DELAY'):
                    sleep(float(line[6:]) / 1000)

                else :
                    parseLine(line)
                    exec("\n".join(translated_list))
                    translated_list.clear()
                    sleep(float(defaultDelay) / 1000)

            # End with a NULL command to release all keys and avoid a endless string
            write_report(NULL_CHAR * 8)

    except OSError as e:
        print("There's no file!")
