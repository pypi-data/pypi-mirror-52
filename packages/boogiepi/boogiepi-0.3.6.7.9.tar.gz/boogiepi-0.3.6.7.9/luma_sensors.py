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
import signal
import string
import subprocess
import sys
import time
from collections import Counter
from logging.handlers import RotatingFileHandler
from subprocess import PIPE, Popen

import bme680
import numpy as np
from cpuinfo import get_cpu_info
from gpiozero import CPUTemperature
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core.virtual import terminal
from luma.oled.device import sh1106

#! Configuration options:
__updated__ = "2019-09-08 18:22:45.515"
NAME = "luma_sensors"  # * This script's name for logging purposes
DESCRIPTION = "Outputs sensor data to oled panel"
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
s_logs = logging.INFO  # * Logging level displayed in shell
f_logs = logging.DEBUG  # * Logging level written to logfile
logFile = f"{SCRIPT_PATH}/logs/{NAME}.log"  # * Where to put the log file
max_log = 100  # * Maximum size of individual log file
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

#! Spin up sensors and displays
serial = i2c(port=1, address=0x3C)
device = sh1106(serial, rotate=2, width=128, height=128, mode="1")
sensor = bme680.BME680()
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
device.clear()
bright = 255
br_level = 100
pmax = 100
pcount = 0
psave = False
term = terminal(device)
loop_num = 0

#! Extracts numbers from strings


def parseStr(x):
    return (
        x.isalpha()
        and x
        or x.isdigit()
        and int(x)
        or x.isalnum()
        and x
        or len(set(string.punctuation).intersection(x)) == 1
        and x.count(".") == 1
        and float(x)
        or x
    )


#! Main loop for drawing terminal-styled data output to oled panel
while True:
    logger.info(f"Panel brightness now {br_level}%")
    device.contrast(bright)
    now = datetime.datetime.now()
    today_date = now.strftime("%d %b %y")
    today_time = now.strftime("%H:%M:%S")
    f = open("/sys/class/thermal/thermal_zone0/temp", "r")
    t = f.readline()
    cputemp = "CPU temp: " + t
    cpu = CPUTemperature()
    cputemp = str(round(cpu.temperature, 2))
    oddata = open(f"{SCRIPT_PATH}/odroid-data", "r")
    for line in oddata:
        if "," in line:
            oddoutput = str(line)
    oddata.close()
    oddoutput = re.search(r" .*C", oddoutput).group()
    oddoutput = oddoutput.strip()
    for key, value in get_cpu_info().items():
        # // logger.debug("{0}: {1}".format(key, value))
        if key == "hz_actual":
            myfreq = re.findall("\d+\.\d+", value)
            myfreq = str(myfreq[0])
            myfreq = parseStr(myfreq)
    if sensor.get_sensor_data():
        mytemp = sensor.data.temperature
        mytemp = (mytemp * 9 / 5) + 32
        mytemp = str(round(mytemp, 2))
        mypres = sensor.data.pressure
        mypres = str(round(mypres, 2))
        myhumid = sensor.data.humidity
        myhumid = str(round(myhumid, 2))

    #! Begin printing data
    # // term.println("Sensor Data:")
    term.println(f"Time:{today_time}")
    logger.debug(f"Time:{today_time}")
    term.println(f"Date:{today_date}")
    logger.debug(f"Date:{today_date}")
    term.println(f"Plex:{myfreq}Ghz, {cputemp}C")
    logger.debug(f"Plex:{myfreq}Ghz, {cputemp}C")
    term.println(f"Pi:{oddoutput}")
    logger.debug(f"Pi:{oddoutput}")
    term.println(f"{mytemp}F, {mypres}hPa")
    logger.debug(f"{mytemp}F, {mypres}hPa")
    term.println(f"{myhumid}% humidity")
    logger.debug(f"{myhumid}% humidity")
    term.animate = False
    for mill in range(0, 1001, 25):
        term.puts("\rPercent: {0:0.1f} %".format(mill / 10.0))
        term.flush()
    loop_num = loop_num + 1
    term.println(" ")
    term.println(f"Cycle {loop_num} complete.")
    term.animate = True
    term.println(" ")

    #! Modify brightness level via simple algorithm
    br_level = round(bright / 255 * 100)
    if bright == 0:
        if pcount >= pmax:
            pcount = 0
            bright = 128
            br_level = 50
            psave = False
        else:
            pcount = pcount + 1
            psave = True
    elif bright < 0:
        bright = 0
        br_level = 0
    else:
        br_level = br_level - 10
        bright = round(br_level / 100 * 255)

    #! Log the cycle completion
    if psave == False:
        logger.info(f"Cycle {loop_num} complete.")
    else:
        logger.info(f"Cycle {loop_num} complete. Powersave {pcount} of {pmax}.")
    if 0 < bright < 255:
        pass
    else:
        bright = 0
        br_level = 0
# /! device.hide()
