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
from pkg_resources import cleanup_resources

import phat_wipe

# ! Configuration options:
__updated__ = "2019-09-24 18:51:33.808"
NAME = "assasinatour"  # * This script's name for logging purposes
DESCRIPTION = "Kills scripts named in arguments via reading their pid file"
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

target = ""
targets = 0
sucess = 0
allpids = {}

# ! Generate a dictionary list of all our pidfiles and their values
try:
    for filename in Path(f"{SCRIPT_PATH}/logs/").glob("**/*.pid"):
        with open(filename, "r") as f:
            tid = int(f.read())  # $ read pid from pidfile
        allpids[str(filename)] = tid
        logger.debug(f"pidfile found {filename}({tid})")
except:
    logger.error("Unable to parse pidfiles to dictionary")


def clean_shim():
    #! Wipe and turn off the ledshim display
    try:
        phat_wipe.clearshim()
        logger.info("Successfully cleared ledshim.")
    except:
        logger.error("An exception occurred while clearing ledshim.")


def clean_oled():
    #! Wipe and turn off the oled display
    try:
        phat_wipe.clearoled()
        logger.info("Successfully cleared oled.")
    except:
        logger.error("An exception occurred while clearing oled.")


def clean_stuff():
    #! Wipe and turn off both the ledshim and oled display
    try:
        phat_wipe.run()
        logger.info("Successfully cleared displays.")
    except:
        logger.error("An exception occurred while clearing displays.")


def kill_stuff(stuff):
    #! kills the process named in {stuff} through its pidfile
    stuff = str(stuff)
    try:
        with open(f"{SCRIPT_PATH}/logs/{stuff}.pid", "r") as kidfile:
            try:
                kid = int(kidfile.read())
                if psutil.pid_exists(kid):
                    try:
                        os.kill(kid, signal.SIGKILL)
                        logger.info(f"Successfully killed {stuff}({kid}).")
                        return True
                    except:
                        logger.error(
                            f"An error occurred while attempting to kill {stuff}({kid})."
                        )
                        logger.error(sys.exc_info()[0])
                else:
                    logger.warning(f"The process {stuff}({kid}) is not running.")
            except:
                logger.error(f"Could not read pid file for {stuff}.")
    except:
        logger.error(f"Could not open pid file for {stuff}.")
    return False


def is_running(stuff):
    #! checks if the process named in {stuff} is running, through its pidfile
    stuff = str(stuff)
    try:
        with open(f"{SCRIPT_PATH}/logs/{stuff}.pid", "r") as kidfile:
            try:
                kid = int(kidfile.read())
                if psutil.pid_exists(kid):
                    return "True"
                else:
                    return "False"

            except:
                logger.error(f"Could not read pid file for {stuff}.")
    except:
        logger.error(f"Could not open pid file for {stuff}.")
    return "Error"


def scout(payload):
    #! Analyzes and responds to {target}
    target = payload[0]
    targets = payload[1]
    sucess = payload[2]
    if target == "CLEAN":
        targets = targets - 1
        clean_stuff()
    elif target == "OLED":
        targets = targets - 1
        clean_oled()
    elif target == "SHIM":
        targets = targets - 1
        clean_shim()
    else:
        cleaner = os.path.splitext(target)
        target = cleaner[0]
        gotem = kill_stuff(target)
        if gotem == True:
            sucess = sucess + 1
    mission = [target, targets, sucess]
    return mission


def run(myargs):
    #! Runs the assasinatour on {myargs}
    if type(myargs) == list:
        arguments = len(myargs)
        targets = arguments
        position = 0
        sucess = 0
        if arguments == 0:
            logger.error("No targets were given. Nothing to do! \U0001F61E")
            logger.debug(f"{NAME} process exited.")
            sys.exit()
        while arguments > position:
            target = myargs[position]
            payload = [target, targets, sucess]
            mission = scout(payload)
            targets = mission[1]
            sucess = mission[2]
            position = position + 1
    elif type(myargs) == str:
        arguments = 1
        targets = arguments
        target = myargs
        payload = [target, targets, sucess]
        mission = scout(payload)
        targets = mission[1]
        sucess = mission[2]
    else:
        logger.error("Target type is invalid.")
    if targets != 0:
        logger.info(f"Completed {sucess} of {targets} assasinations.")
    logger.debug(f"{NAME} process exited.")


def main():
    #! Initalizes the script for standalone operation
    try:  # & Log the process ID for external access
        mypid = os.getpid()
        myppid = os.getppid()
        logger.debug(f"{NAME} process started.")
        logger.debug(f"The process id of {NAME} is {mypid}")
        logger.debug(f"The parent process id of {NAME} is {mypid}")
        with open(f"{SCRIPT_PATH}/logs/{NAME}.pid", "w+") as pidfile:
            pidfile.write(str(mypid))
        # // pidfile.close()
    except:
        logger.error("There was an exception while generating the pidfile.")
    try:
        myargs = sys.argv
        myargs.pop(0)
        run(myargs)
    except:
        logger.error("There was an exception while initalizing the script.")


if __name__ == "__main__":
    # ? Is the script running independently? Then start main()
    main()
