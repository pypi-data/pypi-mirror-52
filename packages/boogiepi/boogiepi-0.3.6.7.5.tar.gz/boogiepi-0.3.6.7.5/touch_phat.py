# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# TODO: Store jobs in config file to allow changing them without restarting
# TODO: Write code to load jobs from config file

import logging
import os
import signal
import time
from logging.handlers import RotatingFileHandler

import psutil

import assasinatour
import ledshim
import touchphat
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import sh1106

#! Configuration options:
__updated__ = "2019-09-08 17:57:31.417"
NAME = "touch-phat"  # * This script's name for logging purposes
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
CAN_INTERNET = True  # * Whether to use data that expects internet access
screen_on = True  # * Default the screen to on
led_on = True  # * Default the ledshim to on
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


@touchphat.on_touch(["Back", "A", "B", "C", "D", "Enter"])  # ! Touched any pad
def handle_touch(event):
    logger.info(f"Touch detected: {event.name}")


@touchphat.on_release("Enter")  # ! Released the Enter pad
def handle_touch(event):
    logger.info("Showing clock-sensor and Plex-temperature-led modules.")
    screen_on = True
    led_on = True
    kll = [
        "ledshim_cpu_temp",
        "luma_clock",
        "flashlight",
        "luma_sensors",
        "luma_odroid",
    ]
    assasinatour.run(kll)
    assasinatour.clean_stuff()
    os.system(f"{SCRIPT_PATH}/phat_stack &")


@touchphat.on_release("Back")  # ! Released the Back pad
def handle_touch(event):
    logger.info("Running module shutdown scripts.")
    kll = [
        "ledshim_cpu_temp",
        "luma_clock",
        "flashlight",
        "luma_sensors",
        "luma_odroid",
    ]
    assasinatour.run(kll)
    assasinatour.clean_stuff()
    os.system(f"python3 {SCRIPT_PATH}/phat_clear.py &")


@touchphat.on_release("A")  # ! Released the A pad
def handle_touch(event):
    logger.info("Cleaning modules.")
    screen_on = True
    led_on = True
    kll = [
        "ledshim_cpu_temp",
        "luma_clock",
        "flashlight",
        "luma_sensors",
        "luma_odroid",
    ]
    assasinatour.run(kll)
    assasinatour.clean_stuff()


@touchphat.on_release("B")  # ! Released the B pad
def handle_touch(event):
    screen_on = True
    led_on = False
    kll = [
        "ledshim_cpu_temp",
        "luma_clock",
        "flashlight",
        "luma_sensors",
        "luma_odroid",
    ]
    assasinatour.run(kll)
    assasinatour.clean_oled()
    # //os.system(f'python3 {SCRIPT_PATH}/phat_quick_clear.py')
    logger.info("Displaying flashlight.")
    os.system(f"python3 {SCRIPT_PATH}/flashlight.py &")


@touchphat.on_release("C")  # ! Released the C pad
def handle_touch(event):
    screen_on = True
    led_on = False
    kll = ["luma_clock", "flashlight", "luma_sensors", "luma_odroid"]
    assasinatour.run(kll)
    assasinatour.clean_oled()
    logger.info("Displaying Sensor readings.")
    os.system(f"python3 {SCRIPT_PATH}/luma_sensors.py &")


@touchphat.on_release("D")  # ! Released the D pad
def handle_touch(event):
    screen_on = True
    led_on = True
    kll = ["ledshim_cpu_temp", "flashlight"]
    assasinatour.run(kll)
    assasinatour.clean_shim()
    logger.info("Showing Plex-temperature-led module.")
    os.system(f"python3 {SCRIPT_PATH}/ledshim_cpu_temp.py &")
    screen_on = False
    led_on = True


while True:
    try:
        signal.pause()
    except:
        try:
            time.sleep(1)
        except:
            logger.error("Keep-alive crashed! Script may have hung!")
            sys.exit()

sys.exit()
