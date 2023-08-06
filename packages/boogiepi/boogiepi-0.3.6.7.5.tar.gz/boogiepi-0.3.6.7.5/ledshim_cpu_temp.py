# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import json
import logging
import os
import re
import threading
import time
from logging.handlers import RotatingFileHandler
from subprocess import PIPE, Popen

import ledshim
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

#! Configuration options:
__updated__ = "2019-09-08 18:04:13.399"
NAME = "ledshim_cpu_temp"  # $ Script name used for logging
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
IOT_ON = False  # $ Toggle for iot features
IOT_TIME = 60  # $ Delay between iot updates in seconds
REFRESH_TIME = 0.1  # $ Delay between led refreshes
s_logs = logging.WARNING  # $ Logging level displayed in shell
f_logs = logging.INFO  # $ Logging level written to logfile
logFile = f"{SCRIPT_PATH}/logs/{NAME}.log"  # $ Where to put the log file
# $ Local shadow of the data pushed to iot
shadowFile = f"{SCRIPT_PATH}/logs/shim.data"
max_log = 100  # $ Maximum size of individual log file in kilobytes
max_backups = 2  # $ Nuumber of backups to keep of log file
oddoutput = "0"
str_temp = "UNDEFINED"
str_ltemp = "UNDEFINED"
iot_running = False
stop_threads = False

#! Set up the logger
logger = logging.getLogger(NAME)  # * Create the logger
logger.setLevel(logging.DEBUG)
max_log = max_log * 1024
fh = RotatingFileHandler(
    logFile, mode="a", maxBytes=max_log, backupCount=max_backups, encoding=None, delay=0
)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
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

#! Set up the IOT client


def init_iot():
    myMQTTClient = AWSIoTMQTTClient(NAME, useWebsocket=True)
    # ? aw2j4vtnh9bs8-ats.iot.us-east-2.amazonaws.com
    myMQTTClient.configureEndpoint("aw2j4vtnh9bs8-ats.iot.us-east-1.amazonaws.com", 443)
    myMQTTClient.configureCredentials("/home/pi/.aws/AmazonRootCA1.pem")
    myMQTTClient.configureIAMCredentials(
        "AKIA6JQLW7H3YQS7BCW4", "apeZZMFYoHF8RoEwTdAhdJw1RJiL9sfjoJrWot0F"
    )
    # * Infinite offline Publish queueing
    myMQTTClient.configureOfflinePublishQueueing(-1)
    myMQTTClient.configureDrainingFrequency(2)  # * Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # * 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # * 5 sec
    return myMQTTClient


def do_shadowFile(jtemp):
    dodata = open(shadowFile, "a+")
    dodata.write(jtemp + "\n")
    dodata.close()


def get_iot(self, params, message):
    #! Receive iot stuff and do things with it
    logger.info("Received a new message: ")
    logger.info(message.payload)
    logger.info("from topic: ")
    logger.info(message.topic)


def do_iot_CPUtemp():
    #! Do/publish iot stuff
    global iot_running
    global str_temp
    global str_ltemp
    global IOT_TIME
    if iot_running == False:
        iot_running = True
        if IOT_ON == False:
            logger.debug("IOT BLOCKED - IOT is turned off.")
        else:
            try:
                myMQTTClient.connect()  # ! Connect to the iot server on aws
                # * Format our data to JSON
                jtemp = {"blueTemp": str_temp, "piTemp": str_ltemp}
                jtemp = json.dumps(jtemp)
                do_shadowFile(jtemp)  # ! Publish a copy to the shadowFile
                # ! Publish to the iot server
                myMQTTClient.publish("CPUtemp", jtemp, 0)
                myMQTTClient.disconnect()  # ! Close the connection to the iot server
                logger.info(f"Did an iot: Published blue[{str_temp}] rasp[{str_ltemp}]")
            except:
                logger.error("An exception occurred during IOT push!")
        # ! Wait for the specified time between published messages
        time.sleep(IOT_TIME)
        iot_running = False


def do_thread(lock):
    #! Make a new thread for iot
    global stop_threads
    # //lock.acquire()
    logger.debug("Started a new thread")
    if stop_threads == False:
        do_iot_CPUtemp()
    # //lock.release()


def get_remote_cputemp():  # ! Get remote cpu temp from odroid-data file
    # * THIS SECTION READS THE PLEX SERVER'S CPU
    try:
        global str_temp
        temp = 0
        oddoutput = "0 0 0 0 0 0 0 0"
        oddata = open(f"{SCRIPT_PATH}/odroid-data", "r")
        for line in oddata:
            if "," in line:
                oddoutput = str(line)
        oddata.close()
        oddnums = re.findall("\d*\.?\d+", oddoutput)
        oddspeed = oddnums[3]
        oddtemp = oddnums[4]
        temp = float(oddtemp)
        str_temp = str(oddtemp)
        str_speed = str(oddspeed)
        logger.debug(
            f"Got remote CPU temperature of {str_temp}C running at {str_speed}Mhz"
        )
    except:
        logger.warning("An exception occurred in the get_remote_cputemp function!")
        temp = 0
    return temp


def get_local_cputemp():  # ! Get local cpu temp with vcgencmd
    # * USE LOCAL CPU
    try:
        global str_ltemp
        ltemp = 0
        process = Popen(["vcgencmd", "measure_temp"], stdout=PIPE)
        output, _error = process.communicate()
        output = output.decode()
        pos_start = output.index("=") + 1
        pos_end = output.rindex("'")
        ltemp = float(output[pos_start:pos_end])
        str_ltemp = str(ltemp)
        logger.debug(f"Got local CPU temperature of {str_ltemp}C")
    except:
        logger.warning("An exception occurred in the get_local_cputemp function!")
        ltemp = 0
    return ltemp


def show_graph(v, r, g, b):  # ! Make a pretty graph
    # TODO Right now we're manually setting colors to specific temperature ranges
    # TODO Eventually we should use math to calculate the colors for a more seamless blend
    # TODO This will use less code and hopefully look prettier!
    try:
        v *= ledshim.NUM_PIXELS
        for x in range(ledshim.NUM_PIXELS):
            if v < 0:
                r, g, b = 0, 0, 0
            else:
                if 7 < x < 15:
                    r, g, b = 0, 255, 0
                    # //r, g, b = [int(min(v, 1.0) * c) for c in [r, g, b]]
                elif x < 3:
                    r, g, b = 0, 0, 255
                elif 3 <= x < 5:
                    r, g, b = 150, 150, 255
                elif x == 5:
                    r, g, b = 200, 200, 200
                elif x == 6:
                    r, g, b = 0, 255, 150
                elif x == 7:
                    r, g, b = 0, 255, 0
                elif x == 15:
                    r, g, b = 128, 255, 0
                elif 15 < x < 20:
                    r, g, b = 255, 255, 0
                elif x == 20:
                    r, g, b = 255, 128, 0
                else:
                    r, g, b = 255, 0, 0
            ledshim.set_pixel(x, r, g, b)
            v -= 1
    except:
        logger.warning("An exception occurred in the show_graph function!")
        pass


def show_hot_graph(v, r, g, b):  # ! Do the RED thing when it's really hot
    try:
        v *= ledshim.NUM_PIXELS
        for x in range(ledshim.NUM_PIXELS):
            if v < 0:
                r, g, b = 0, 0, 0
            else:
                r, g, b = [int(min(v, 1.0) * c) for c in [r, g, b]]
            ledshim.set_pixel(x, r, g, b)
            v -= 1
    except:
        logger.warning("An exception occurred in the show_hot_graph function!")
        pass


def show_local_led(vloca):  # ! Color the last pixel
    # TODO Right now we're manually setting colors to specific temperature ranges
    # TODO Eventually we should use math to calculate the colors for a more seamless blend
    # TODO This will use less code and hopefully look prettier!
    try:
        xloca = ledshim.NUM_PIXELS - 1
        if vloca < 0:
            ledshim.set_pixel(xloca, 0, 0, 0)
        elif 0 < vloca <= 0.45:
            ledshim.set_pixel(xloca, 0, 0, 255)
        elif 0.45 < vloca <= 0.46:
            ledshim.set_pixel(xloca, 150, 150, 255)
        elif 0.46 < vloca <= 0.47:
            ledshim.set_pixel(xloca, 255, 255, 255)
        elif 0.47 < vloca <= 0.48:
            ledshim.set_pixel(xloca, 75, 255, 75)
        elif 0.48 < vloca <= 0.50:
            ledshim.set_pixel(xloca, 0, 255, 0)
        elif 0.50 < vloca <= 0.53:
            ledshim.set_pixel(xloca, 0, 150, 50)
        elif 0.53 < vlocal <= 0.55:
            ledsh.set_pixel(xloca, 0, 150, 150)
        elif 0.55 < vloca <= 0.60:
            ledshim.set_pixel(xloca, 50, 255, 255)
        elif 0.60 < vloca <= 0.7:
            ledshim.set_pixel(xloca, 250, 100, 100)
        elif vloca > 0.7:
            ledshim.set_pixel(xloca, 255, 0, 0)
        else:
            ledshim.set_pixel(xloca, 255, 255, 255)
    except:
        logger.warning("An exception occurred in the show_local_led function!")
        pass


#! Start the main process


def main():
    global iot_running
    myMQTTClient = init_iot()
    ledshim.set_clear_on_exit()  # & Tell the ledshim to clear when we exit
    logger.info("Started ledshim CPU Temperature Grapher")
    while True:
        try:
            v = 0
            vloca = 0
            v = get_remote_cputemp() / 100.0  # % Make our values percentages
            vloca = get_local_cputemp() / 100.0
            if v >= 0.95:  # ? If temp is hot enough..
                ledshim.set_brightness(0.3)
                show_hot_graph(v, 255, 0, 0)  # ! do bright red graph
            else:  # ? Otherwise:
                ledshim.set_brightness(0.15)
                show_graph(v, 0, 255, 0)  # ! Show the normal graph
            show_local_led(vloca)  # ! Show the local cpu led
            ledshim.show()  # ! Display the updated graphs
            logger.debug("Refreshed LEDs successfully.")
            #! Call iot Threading stuff
            # /* We aren't using lock anymore but keeping it for reference
            lock = threading.Lock()
            t2 = threading.Thread(target=do_thread, args=(lock,))
            t2.start()
            num_threads = threading.active_count()  # % Count the concurrent threads
            logger.debug(f"There are {num_threads} concurrent threads")
            if num_threads >= 5:  # ? Do we have to many threads open?
                stop_threads = True  # ! Stop making more threads
            else:  # ? Reasonable number of threads?
                stop_threads = False  # ! Turn on the thread spawner
        except:
            logger.warning("An exception occurred in the main loop!")
            pass
        # ! Wait for the specified refresh time before repeating the loop
        time.sleep(REFRESH_TIME)


if __name__ == "__main__":
    main()
