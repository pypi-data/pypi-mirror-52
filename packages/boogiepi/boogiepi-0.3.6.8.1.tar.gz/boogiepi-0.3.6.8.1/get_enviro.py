# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

'''
Notes:
    So I've been using pyowm for weather forcasts and other weather-
    related data. It has somne drawbacks not the least of which is
    the limits imposed by the free license and the hoops I've had to
    jump through to use the limited data.
    At this point I think it might be a good idea to start experimenting
    with darksky using one of the available libraries.
    To begin with:
        darksky_weather
    Other options:
        darkskylib
        ForcastIO Python 3
    If any of these work out, I can begin transissioning other parts of the
    package from pyowm to darksky.
'''

import datetime
import logging
import os
import re
import socket
import sys
import time
from logging.handlers import RotatingFileHandler
from os import PathLike
from shutil import copyfile
from subprocess import PIPE, Popen

import geocoder
import ntplib
import pyowm
from requests import get

#! Configuration options:
__updated__ = "2019-09-12 23:45:32.567"
NAME = "get_enviro"
DEVICE_NAME = "pi"
DESCRIPTION = "environment data from sensors and weather net"
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
HAS_SENSORS = True
CAN_ODROID = True
CAN_INTERNET = True
SILENT = True
REFRESH_TIME = 0
OWM_APIKEY = "dcf3760c23dca5b013656cad67f6d72a"
DATA_FILE = f"{SCRIPT_PATH}/logs/{NAME}.data"
s_logs = logging.INFO  # * Logging level displayed in shell
f_logs = logging.DEBUG  # * Logging level written to logfile
logFile = f"{SCRIPT_PATH}/logs/{NAME}.log"  # * Where to put the log file
max_log = 100  # * Maximum size of individual log file
max_backups = 2  # * Nuumber of backups to keep of log file

if HAS_SENSORS == True:
    import bme680

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


def blockPrint():
    sys.stdout = open(os.devnull, "w")


def enablePrint():
    sys.stdout = sys.__stdout__


def degToCompass(num):
    val = int((num / 22.5) + 0.5)
    arr = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    return arr[(val % 16)]


def get_ip():
    return (
        (
            [
                ip
                for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                if not ip.startswith("127.")
            ]
            or [
                [
                    (s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close())
                    for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
                ][0][1]
            ]
        )
        + ["no IP found"]
    )[0]


#! Initalizes the script for standalone operation
try:  # & Log the process ID for external access
    mypid = os.getpid()
    myppid = os.getppid()
    logger.debug(f"{NAME} process started.")
    logger.debug(f"The process id of {NAME} is {mypid}")
    logger.debug(f"The parent process id of {NAME} is {mypid}")
    with open(f"{SCRIPT_PATH}/logs/{NAME}.pid", "w+") as pidfile:
        pidfile.write(str(mypid))
except:
    logger.error("There was an exception while generating the pidfile.")

if HAS_SENSORS == True:
    sensor = bme680.BME680()
    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)

owm = pyowm.OWM(OWM_APIKEY)
CAN_INTERNET = owm.is_API_online()
c = ntplib.NTPClient()
try:
    while True:
        try:
            response = c.request("north-america.pool.ntp.org", version=3)
            ntp_now = str(datetime.datetime.fromtimestamp(response.tx_time))
            the_now = str(datetime.datetime.now())
            the_now = re.sub(r"\s+", ",", the_now)
            the_now = re.sub(r":+", "-", the_now)
            ntp_now = re.sub(r"\s+", ",", ntp_now)
            ntp_now = re.sub(r":+", "-", ntp_now)
        except:
            ntp_now = "none"
        try:
            hostname = socket.gethostname()
            loc_ip = str(get_ip())
        except:
            loc_ip = "none"
        if CAN_INTERNET == True:
            try:
                pub_ip = get("https://api.ipify.org").text
            except:
                pub_ip = "none"
            try:
                try:
                    blockPrint()
                    g = geocoder.ip("me")
                    if g.ok == False:
                        # os.system('clear')
                        g = geocoder.osm("Pittsfield, MA")
                        # print('osm')
                    enablePrint()
                except:
                    g = geocoder.google([42.4501, -73.2454], method="reverse")
                the_here = g.latlng
                the_place = str(g.city + "," + g.state + "," + g.country)
                lat = the_here[0]
                lon = the_here[1]
                try:
                    uvi = owm.uvindex_around_coords(lat, lon)
                    uv_risk = uvi.get_exposure_risk()
                    uv_index = uvi.get_value()
                except:
                    uv_index = "none"
                    uv_risk = "none"
                observation = owm.weather_at_coords(lat, lon)
                the_here = str(lat) + "," + str(lon)
                weather = observation.get_weather()
                the_wind = weather.get_wind()
                if len(the_wind) > 1:
                    try:
                        the_wind = "wind "+degToCompass(the_wind["deg"])+" "+str(the_wind["speed"])+"mph"
                    except:
                        try:
                            the_wind = "wind " + str(the_wind["speed"]) + "mph"
                        except:
                            the_wind = "no wind"
                elif len(the_wind) == 1:
                    try:
                        the_wind = "wind "+str(the_wind["speed"])
                    except:
                        the_wind = "none"
                else:
                    the_wind = "none"
                the_clouds = str(weather.get_clouds()) + "%"
                the_rain = weather.get_rain()
                try:
                    if len(the_rain) != 0:
                        the_rain = str(the_rain["1h"])
                except:
                    the_rain = "no rain"
                the_snow = weather.get_snow()
                try:
                    if len(the_snow) != 0:
                        the_snow = the_snow["3hr"]
                except:
                    the_snow = "no snow"
                the_weather = str(weather.get_detailed_status())
            except:
                the_here = "none"
                the_place = "none"
                the_wind = "none"
                the_clouds = "none"
                the_rain = "none"
                the_snow = "none"
                the_weather = "none"
                if HAS_SENSORS == True:
                    if sensor.get_sensor_data():
                        if sensor.data.heat_stable:
                            try:
                                the_temp = str(sensor.data.temperature) + "C"
                                the_ftemp = (
                                    str(round(float(sensor.data.temperature) * 9 / 5 + 32, 2)) + "F"
                                )
                                the_press = str(sensor.data.pressure) + "hPa"
                                the_humid = str(sensor.data.humidity) + "%RH"
                                the_gas = str(sensor.data.gas_resistance) + "ohms"
                            except:
                                the_temp = "none"
                                the_ftemp = "none"
                                the_press = "none"
                                the_humid = "none"
                                the_gas = "none"
            try:
                the_rtemp = str(weather.get_temperature("fahrenheit")["temp"]) + "F"
                the_rhumid = str(weather.get_humidity()) + "%RH"
                the_rpress = str(round(weather.get_pressure()["press"], 2)) + "hPa"
            except:
                the_rtemp = "none"
                the_rhumid = "none"
                the_rpress = "none"
            try:
                oddata = open(f"{SCRIPT_PATH}/odroid-data", "r")
                for line in oddata:
                    if "," in line:
                        oddoutput = str(line)
                oddata.close()
                oddnums = re.findall("\d*\.?\d+", oddoutput)
                oddspeed = str(oddnums[3]) + "mhz"
                oddtemp = str(round(float(oddnums[4]), 2)) + "C"
            except:
                oddspeed = "none"
                oddtemp = "none"

            try:
                if DEVICE_NAME == 'pi':
                    ltemp = 0
                    process = Popen(["vcgencmd", "measure_temp"], stdout=PIPE)
                    output, _error = process.communicate()
                    output = output.decode()
                    pos_start = output.index("=") + 1
                    pos_end = output.rindex("'")
                    ltemp = float(output[pos_start:pos_end])
                    str_ltemp = str(ltemp) + "C"
                    fltemp = round(ltemp * 9 / 5 + 32, 1)
                    str_fltemp = str(fltemp) + "F"
                    process = Popen(["vcgencmd", "measure_clock arm"], stdout=PIPE)
                    output, _error = process.communicate()
                    output = output.decode()
                    pos_start = output.index("=") + 1
                    pos_end = len(output)
                    lspeed = float(output[pos_start:pos_end])
                    lspeed = round(lspeed / 1000000)
                    lspeed = str(lspeed) + "mhz"
                else:
                    ltemp = "none"
                    str_ltemp = "none"
                    fltemp = "none"
                    str_fltemp = "none"
                    lspeed = "none"
            except:
                ltemp = "none"
                lspeed = "none"
        if HAS_SENSORS == False:
            the_ftemp = "none"
            the_humid = "none"
            the_press = "none"
            the_gas = "none"
        if CAN_ODROID == False:
            oddspeed = "none"
            oddtemp = "none"
        the_enviro = {
            "name": NAME,
            "description": DESCRIPTION,
            "sys_time": the_now,
            "ntp_time": ntp_now,
            "hostname": hostname,
            "loc_ip": loc_ip,
            "pub_ip": pub_ip,
            "geo_location": the_here,
            "geo_place": the_place,
            "weather": the_weather,
            "wthr_temperature": the_rtemp,
            "wthr_humidity": the_rhumid,
            "wthr_pressure": the_rpress,
            "wthr_wind": the_wind,
            "wthr_clouds": the_clouds,
            "uv_index": uv_index,
            "uv_risk": uv_risk,
            "wthr_rain": the_rain,
            "wthr_snow": the_snow,
            "snsr_temperature": the_ftemp,
            "snsr_humidity": the_humid,
            "snsr_pressure": the_press,
            "snsr_vo2_gas": the_gas,
            f"{DEVICE_NAME}_speed": lspeed,
            f"{DEVICE_NAME}_temperature": str_ltemp,
            "odroid_speed": oddspeed,
            "odroid_temperature": oddtemp,
        }
        dfile = open(DATA_FILE, "w")
        for v in the_enviro:
            data = str(v) + "::" + str(the_enviro[v])
            dfile.write(data + "\n")
            if v != "name":
                if v != "description":
                    logger.info(f"Data collected - {data}")
        dfile.close()
        bkpfile = DATA_FILE + ".0"
        copyfile(DATA_FILE, bkpfile)
        if SILENT == False:
            dfile = open(bkpfile, "r")
            print("\033[1;34;40m" + str(dfile.read()))
            print("\033[0;37;40m")
            dfile.close()
        if REFRESH_TIME == 0:
            if HAS_SENSORS == True:
                sensor.set_gas_status(bme680.DISABLE_GAS_MEAS)
            sys.exit()
        else:
            time.sleep(REFRESH_TIME)

except KeyboardInterrupt:
    pass
