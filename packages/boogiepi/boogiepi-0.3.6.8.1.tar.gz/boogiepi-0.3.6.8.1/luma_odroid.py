# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import colorsys
import datetime
import io
import logging
import os
import re
import subprocess
import sys
import time
from collections import Counter
from logging.handlers import RotatingFileHandler
from subprocess import PIPE, Popen

import bme680
import numpy as np
from cpufreq import cpuFreq
from cpuinfo import get_cpu_info
from gpiozero import CPUTemperature
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core.virtual import terminal
from luma.oled.device import sh1106

#! Configuration options:
__updated__ = "2019-09-08 18:05:02.933"
NAME = "luma_odroid"  # $ This script's name for logging purposes
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
s_logs = logging.ERROR  # $ Logging level displayed in shell
f_logs = logging.DEBUG  # $ Logging level written to logfile
logFile = f"{SCRIPT_PATH}/logs/{NAME}.log"  # $ Where to put the log file
max_log = 100  # $ Maximum size of individual log file
max_backups = 2  # $ Nuumber of backups to keep of log file

#! Set up the logger
logger = logging.getLogger(NAME)  # * Create the logger
logger.setLevel(logging.DEBUG)
max_log = max_log * 1024
fh = RotatingFileHandler(
    logFile, mode="a", maxBytes=max_log, backupCount=max_backups, encoding=None, delay=0
)
ch = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - luma_odroid - %(levelname)s - %(message)s"
)  # * Set logger formatting
ch.setFormatter(formatter)
fh.setFormatter(formatter)
ch.setLevel(s_logs)  # * Set the logging levels
fh.setLevel(f_logs)
logger.addHandler(ch)  # * Add the newly configured handlers to the logger
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
device.clear()

term = terminal(device)

oddata = open(f"{SCRIPT_PATH}/odroid-data", "r")
for line in oddata:
    if "," in line:
        oddoutput = str(line)
oddata.close()
oddstuff = re.search(r", .*?C", oddoutput).group()
oddstuff = re.search(r" .*?C", oddstuff).group()
oddtemp = oddstuff.strip()
oddtemp = int("".join(filter(str.isdigit, oddtemp))) / 100
oddtemp = str(oddtemp) + "C"
oddstuff = re.search(r" .*?z", oddoutput).group()
oddspeed = oddstuff.strip()
oddspeed = int("".join(filter(str.isdigit, oddspeed)))
oddspeed = str(oddspeed) + "Mhz"

term.println("Plex:")
term.println(oddspeed)
term.println(oddtemp)
time.sleep(5)

device.hide()
