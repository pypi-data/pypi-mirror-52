# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
import os
import re
import threading
import time
from logging.handlers import RotatingFileHandler
from subprocess import PIPE, Popen

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

#! Configuration options:
__updated__ = "2019-09-08 18:41:22.087"
NAME = "iot_Getter"  # Script name used for logging
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
SILENT = True
REFRESH_TIME = 0
OWM_APIKEY = "dcf3760c23dca5b013656cad67f6d72a"
DATA_FILE = f"{SCRIPT_PATH}/logs/{NAME}.data"
s_logs = logging.INFO  # * Logging level displayed in shell
f_logs = logging.DEBUG  # * Logging level written to logfile
logFile = f"{SCRIPT_PATH}/logs/{NAME}.log"  # * Where to put the log file
max_log = 100  # * Maximum size of individual log file
max_backups = 2  # * Nuumber of backups to keep of log file
iot_on = True  # Toggle for iot features
iot_time = 900  # Delay between iot updates in seconds

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

myMQTTClient = AWSIoTMQTTClient(NAME, useWebsocket=True)
myMQTTClient.configureEndpoint("aw2j4vtnh9bs8-ats.iot.us-east-2.amazonaws.com", 443)
myMQTTClient.configureCredentials("/home/pi/.aws/AmazonRootCA1.pem")
# Infinite offline Publish queueing
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec


def get_iot(self, params, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)


while True:
    myMQTTClient.connect()
    # myMQTTClient.publish("blueCPUtemp", str_temp, 0)
    # myMQTTClient.publish("raspCPUtemp", str_ltemp, 0)
    myMQTTClient.subscribe("blueCPUtemp", 1, get_iot)
    myMQTTClient.unsubscribe("blueCPUtemp")
    myMQTTClient.disconnect()
