# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
    This script does the following:
        More aggressive kills to all the touch_phat subprocesses.
        Flushes and clears both oled panel and ledshim.
"""

import colorsys
import logging
import os
import subprocess
import sys
import time
from logging.handlers import RotatingFileHandler

import ledshim
import numpy as np
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core.virtual import terminal
from luma.oled.device import sh1106

#! Configuration options:
__updated__ = "2019-09-08 18:06:20.136"
NAME = "phat_clear"
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

os.system(
    "sudo pkill -f ledshim_cpu_temp.py & sudo pkill -f luma_clock.py & sudo pkill -f luma_sensors.py & sudo pkill -f luma_odroid"
)

ledshim.set_clear_on_exit()
ledshim.clear()
ledshim.show()

serial = i2c(port=1, address=0x3C)
device = sh1106(serial, rotate=2, width=128, height=128, mode="1")

device.clear()
device.contrast(255)

term = terminal(device)

term.println("Shutting down")
term.println("modules")
term.println(" ")
term.println("ledshim")
term.println("...")


def make_gaussian(fwhm):
    x = np.arange(0, ledshim.NUM_PIXELS, 1, float)
    y = x[:, np.newaxis]
    x0, y0 = 3.5, (ledshim.NUM_PIXELS / 2) - 0.5
    fwhm = fwhm
    gauss = np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)
    return gauss


for z in list(range(1, 10)[::-1]) + list(range(1, 10)):
    fwhm = 15.0 / z
    gauss = make_gaussian(fwhm)
    start = time.time()
    y = 4
    for x in range(ledshim.NUM_PIXELS):
        h = 0.5
        s = 1.0
        v = gauss[x, y]
        rgb = colorsys.hsv_to_rgb(h, s, v)
        r, g, b = [int(255.0 * i) for i in rgb]
        ledshim.set_pixel(x, r, g, b)
    ledshim.show()
    end = time.time()
    t = end - start
    if t < 0.04:
        time.sleep(0.04 - t)

ledshim.clear()
ledshim.show()

term.println("OLED display")
term.println("...")

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="white")

ledshim.clear()
ledshim.show()
device.hide()
device.cleanup()
