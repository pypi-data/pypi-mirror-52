# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import multiprocessing
import os
import sys
import time
import logging
from datetime import datetime

import psutil

import ledshim
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import sh1106
from logging.handlers import RotatingFileHandler

#! Configuration options:
__updated__ = "2019-09-24 16:46:52.068"
NAME = "flashlight"
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
s_logs = logging.INFO  # * Logging level displayed in shell
f_logs = logging.DEBUG  # * Logging level written to logfile
logFile = f"{SCRIPT_PATH}/logs/{NAME}.log"  # * Where to put the log file
max_log = 100  # * Maximum size of individual log file
max_backups = 2  # * Number of backups to keep of log file
#! Set up the logger
logger = logging.getLogger(NAME)
logger.setLevel(logging.DEBUG)
max_log = max_log * 1024
fh = RotatingFileHandler(
    logFile, mode="a", maxBytes=max_log, backupCount=max_backups, encoding=None, delay=0
)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
ch.setLevel(s_logs)
fh.setLevel(f_logs)
logger.addHandler(ch)
logger.addHandler(fh)

#! Log the process ID for external access
mypid = os.getpid()
logger.debug(f"{NAME} process started.")
logger.debug(f"Last updated: {__updated__}")
logger.debug(f"The process id of {NAME} is {mypid}")
with open(f"{SCRIPT_PATH}/logs/{NAME}.pid", "w+") as pidfile:
    pidfile.write(str(mypid))

serial = i2c(port=1, address=0x3C)
device = sh1106(serial, rotate=2, width=128, height=128, mode="1")
device.contrast(255)
ledshim.set_clear_on_exit()  # Tell the ledshim to clear when we exit
ledshim.clear()
for x in range(ledshim.NUM_PIXELS):
    ledshim.set_pixel(x, 255, 255, 255)
ledshim.show()


with canvas(device, dither=True) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="white")
while True:
    try:
        time.sleep(1)
    except:
        device.cleanup()
        ledshim.clear()
        ledshim.hide()
        break
