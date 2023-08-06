# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import glob
import logging
import os
import signal
import sys
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

import psutil

import assasinatour

# ! Configuration options:
__updated__ = "2019-09-11 16:14:19.060"
NAME = "statinatour"  # * This script's name for logging purposes
DESCRIPTION = "Gets a variety of statistics"
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
s_logs = logging.INFO  # * Logging level displayed in shell
f_logs = logging.DEBUG  # * Logging level written to logfile
logFile = f"{SCRIPT_PATH}/logs/{NAME}.log"  # * Where to put the log file
max_log = 100  # * Maximum size of individual log file in kilobytes
max_backups = 2  # * Number of backups to keep of log file
# ! Set up the logger
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


def is_running(script):
    script_running = assasinatour.is_running(script)
    if script_running == "True":
        return f"{script} is running."
    elif script_running == "False":
        return f"{script} is NOT running."
    else:
        return f"{script} could not be found."


def get_cpu_percent():
    cpu_percent = str(psutil.cpu_percent()) + "%"
    return cpu_percent


def get_cpu_freq():
    cpu_freq = psutil.cpu_freq()
    return cpu_freq


def get_disk_usage():
    disk_usage = psutil.disk_usage("/")
    return disk_usage


def get_current_freq():
    current_freq = str(get_cpu_freq()[0]) + "Mhz"
    return current_freq


def get_disk_percent():
    disk_percent = str(get_disk_usage()[3]) + "%"
    return disk_percent


def main():
    try:
        cpuPercent = get_cpu_percent()
        print(f"CPU load: {cpuPercent}")
    except:
        print("CPU load: Unknown")
    try:
        cpuFreq = str(get_cpu_freq()[0]) + "Mhz"
        print(f"CPU freqency: {cpuFreq}")
    except:
        print("CPU frequency: Unknown")
    try:
        diskPercent = get_disk_percent()
        print(f"Disk usage: {diskPercent}")
    except:
        print("Disk usage: Unknown")

    try:
        numargs = len(sys.argv)
        if numargs > 1:
            myargs = str(sys.argv[1])
            if myargs != "":
                print(is_running(myargs))
    except:
        print("There was an error parsing arguments.")


if __name__ == "__main__":
    main()
