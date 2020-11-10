import os
import logging
import sys
import time

command='bash start.sh run-proxy'
mode='snet_proxy'

try:
    os.system('docker rm -f '+str(mode))
except:
    logging.exception("message")


try:
    os.system(command)
except:
    logging.exception("message")
