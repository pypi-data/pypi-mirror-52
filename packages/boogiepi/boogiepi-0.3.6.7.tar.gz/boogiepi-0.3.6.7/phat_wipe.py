# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import logging
from logging.handlers import RotatingFileHandler

import ledshim
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import sh1106

#! Configuration options:
__updated__ = "2019-09-24 16:46:27.722"
NAME = "phat_wipe"  # * This script's name for logging purposes
DESCRIPTION = "Tool for wiping phat_stack displays"
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
s_logs = logging.INFO  # * Logging level displayed in shell
f_logs = logging.DEBUG  # * Logging level written to logfile
logFile = f"{SCRIPT_PATH}/logs/{NAME}.log"  # * Where to put the log file
max_log = 100  # * Maximum size of individual log file in kilobytes
max_backups = 2  # * Nuumber of backups to keep of log file

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


def clearoled():
    serial = i2c(port=1, address=0x3C)
    device = sh1106(serial, rotate=2, width=128, height=128, mode="1")
    device.clear()
    device.hide()


def clearshim():
    #    ledshim.hide()
    for x in range(ledshim.NUM_PIXELS):
        ledshim.set_pixel(x, 0, 0, 0)
    ledshim.clear()
    ledshim.show()


def run():
    clearoled()
    clearshim()


def main():
    run()


if __name__ == "__main__":
    main()
