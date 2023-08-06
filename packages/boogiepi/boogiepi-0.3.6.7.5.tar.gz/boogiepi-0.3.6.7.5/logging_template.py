# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import logging
from logging.handlers import RotatingFileHandler

#! Configuration options:
__updated__ = "2019-09-08 18:54:06.085"
NAME = "logging_template"
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

# ! Log the process ID for external access
mypid = os.getpid()
logger.debug(f"{NAME} process started.")
logger.debug(f"The process id of {NAME} is {mypid}")
logger.debug(f"Last updated: {__updated__}")
with open(f"{SCRIPT_PATH}/logs/{NAME}.pid", "w+") as pidfile:
    pidfile.write(str(mypid))

#^ Copy the above code and set NAME="Your_script_name"

#! Sample logging code:
logger.info("Welcome to {NAME}!")
logger.info("This snippet will generate logs and logfiles.")
logger.info("It will also generate a pidfile to track the pid({mypid})")
logger.info("")
logger.info(f"Log path: {logFile}")
logger.warning(f"{NAME} will now exit.")
