# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

#! Important
# ^ Highlight
# // Strikethrough
# /! Important Strikethrough
# * Note
# ? Question
# $ Value
# % Math
# & And
# + Plus
# = Equal

import datetime
import logging
import math
import os
import re
import sys
import threading
import time
from collections import Counter
from logging.handlers import RotatingFileHandler
from subprocess import PIPE, Popen

import psutil

import bme680
import geocoder
import pyowm
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageFont

#! Configuration options:
__updated__ = "2019-09-08 18:04:23.523"
NAME = "luma-clock"  # $ This script's name for logging purposes
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
CAN_INTERNET = True  # $ Whether to use data that expects internet access
WEATHER_REFRESH = 60  # $ How many seconds to wait between weather forcasts
REFRESH_TIME = 0.1  # $ Screen refresh rate
SCREEN_BRIGHTNESS = 255  # $ Brightness (contrast) of the screen 0-255
s_logs = logging.ERROR  # $ Logging level displayed in shell
f_logs = logging.INFO  # $ Logging level written to logfile
logFile = f"{SCRIPT_PATH}/logs/{NAME}.log"  # $ Where to put the log file
max_log = 100  # $ Maximum size of individual log file in kilobytes
max_backups = 2  # $ Nuumber of backups to keep of log file

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


def most_frequent(List):
    #! Find the most frequent string in List
    # % Count all the occurences of each string
    occurence_count = Counter(List)
    # % Return the most common occurence
    return occurence_count.most_common(1)[0][0]


def get_average(List):
    #! Get the average of all the numbers in List
    mySum = 0
    x = 0
    for num in List:  # % Add up all the numbers in List
        # //print (num)
        x = x + 1
        mySum = float(mySum) + float(num)
    average = mySum / x  # % Divide the sum of List by the count of List
    str_average = str(average)
    logger.debug(f"Found average: {str_average}.")
    return average  # % Return the average of the numbers in List


def change_brightness(Level):
    #! Change the brightness of the oled panel to Level
    new_level = Level
    # * Change the contrast/brightness of oled panel
    device.contrast(new_level)
    logger.info(f"Changed OLED panel brightness to {new_level}.")


def do_weather():
    global owm, cur_condi, condi, owm_running, owm_humid, owm_temp
    global CAN_INTERNET, SCREEN_BRIGHTNESS, WEATHER_REFRESH
    if owm_running == False:  # & Make sure we're the only do_weather running
        if CAN_INTERNET == True:  # ? Do we have internet access?
            owm_running = (
                True
            )  # & Notify the main thread that we're doing a weather observation
            logger.info("Started weather update.")
            mygeocode = geocoder.ip("me")  # * Get the geolocation
            mylatlng = [42.4501, -73.2454]
            # //mylatlng = mygeocode.latlng #* Format it to [lat,long]
            observation = owm.weather_at_coords(
                mylatlng[0], mylatlng[1]
            )  # * Get the observation
            # //mywid = observation.get_ID() #* Get the weather location ID
            # * Read the weather from the observation
            cur_weather = observation.get_weather()
            #! Get the forcasted weather:
            # TODO: Get this to work reliably with acquired location instead of manual. Can also use 'zip, us'
            # TODO: Can't continuously request geocoder, we'll get blocked
            # TODO: Instead, get ip and save it with a datetime to refresh only every few hours or so
            fc = owm.three_hours_forecast("West Stockbridge, US")
            f = fc.get_forecast()  # ! New method to grab the most common conditions
            iweather = []
            itemp = []  # $ Initialize the weather dictionaries
            ihumid = []
            i = 0
            for weather in f:
                i = i + 1
                if i == 1:
                    cur_weather = weather

                if i < 10:
                    # $ Fill the weather status dict
                    iweather.append(str(weather.get_status()))
                    mytemp = weather.get_temperature("fahrenheit")
                    temp = mytemp["temp"]
                    # $ Fill the weather temperature dict
                    itemp.append(float(temp))
                    # $ Fill the weather humidity dict
                    ihumid.append(float(weather.get_humidity()))
            # //print(iweather)
            condi = most_frequent(iweather)  # % Get the average conditions
            # % Get the average temperature
            owm_temp = round(get_average(itemp), 2)
            # % Get the average humidity
            owm_humid = round(get_average(ihumid), 2)
            # TODO: Should get ozone levels: (BROKEN or UNSUPPORTED)
            # //o3 = owm.ozone_around_coords(42.4501, -73.2454) #coordinates for Pittsfield
            # $ Make things prettier by adding descriptors
            owm_humid = str(owm_humid) + "% RH"
            owm_temp = str(owm_temp) + "F"
            cur_condi = str(cur_weather.get_detailed_status())
        logger.info(f"Weather updated. Current Conditions:{cur_condi}.")
        # ! Sets the delay between weather observations
        time.sleep(WEATHER_REFRESH)
        # //print(SCREEN_BRIGHTNESS)
        if (
            SCREEN_BRIGHTNESS > 0
        ):  # % This and the one in main() produce a SCREEN_BRIGHTNESS
            # % countdown that ends with the script closing
            # % This is meant to reduce burn-in on the oled
            # % Decrease oled brightness by 1 every weather cycle
            SCREEN_BRIGHTNESS = SCREEN_BRIGHTNESS - 1
            # * Change the screen brightness
            change_brightness(SCREEN_BRIGHTNESS)
        else:
            sys.exit()
        owm_running = False


def do_thread(lock):
    #! Start a weather data thread
    # TODO: This can prolly be condensed down to just the do_weather function.
    # //lock.acquire()
    # //logger.debu1g('Started a new thread')
    do_weather()  # $ Do a refresh of weather/forcast data
    # //lock.release()


def do_Font():
    #! Selects font options and returns an ImageFont object
    # * Font options for big digital clock:
    # //FontTemp = ImageFont.truetype(f'{SCRIPT_PATH}/fonts/FreePixel.ttf',24)
    FontTemp = ImageFont.truetype(f"{SCRIPT_PATH}/fonts/code2000.ttf", 22)
    # //FontTemp = ImageFont.truetype(f'{SCRIPT_PATH}/fonts/ProggyTiny.ttf',32)
    # //FontTemp = ImageFont.truetype(f'{SCRIPT_PATH}/fonts/pixelmix.ttf',18)
    # //FontTemp = ImageFont.truetype(f'{SCRIPT_PATH}/fonts/miscfs_.ttf',24)
    return FontTemp  # $ Load the Font settings selected above


def posn(angle, arm_length):
    #! Calculates the arm angles for analog clock
    dx = int(math.cos(math.radians(angle)) * arm_length)
    dy = int(math.sin(math.radians(angle)) * arm_length)
    return (dx, dy)


def main():
    global NAME, condi, cur_condi  # ! Set a buttload of variables.
    today_last_time = "Unknown"
    sensor.set_humidity_oversample(bme680.OS_2X)  # ! Sensor variables..
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)  # ! Gas sensor variables..
    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)
    start_time = time.time()  # $ Set time variables...
    curr_time = time.time()
    burn_in_time = 750
    burn_in_data = []
    air_quality_score = "0"  # $ AQI and baseline variables....
    gas_baseline = 0
    hum_baseline = 40.0
    hum_weighting = 0.25
    mytemp = "00.00F"  # $ Zero string variables......
    mypres = "000.00hPa"
    myhumid = "00.00% RH"
    air_quality_score = "00.00% AQI"
    oddoutput = "00:00:00:  000mhz 00.00C"  # $ Phew, finally!
    while True:  # ! This is the main loop to collect data and refresh display
        try:
            if SCREEN_BRIGHTNESS <= 0:  # ? Is the screen brightness at minimum?
                #! Check the screen brightness and exit if it's at minimum
                sys.exit()  # ^ Exit the script if the screen brightness is set to 0
            #! Spin up the data collector thread
            lock = threading.Lock()
            t2 = threading.Thread(target=do_thread, args=(lock,))
            t2.start()
            # TODO: Use or remove thread counting code
            # //num_threads = threading.active_count()
            # //str_num_threads = str(num_threads)
            now = datetime.datetime.now()  # $ Set now to realtime now
            today_date = now.strftime("%d %b %y")
            today_time = now.strftime("%H:%M:%S")  # % Format datetimes
            short_time = now.strftime("%H:%M")
            if (
                curr_time - start_time < burn_in_time
            ):  # ? Are we still in burn-in process?
                curr_time = time.time()
                if (
                    sensor.get_sensor_data() and sensor.data.heat_stable
                ):  # ? Is the sensor ready?
                    gas = sensor.data.gas_resistance
                    # $ Add another burn-in reading to the List
                    burn_in_data.append(gas)
                    # //logger.debug(f'Gas: {gas} Ohms')
                    gas_baseline = sum(burn_in_data[-50:]) / 50.0
                    mytemp = (
                        sensor.data.temperature
                    )  # $ Get temperature reading from sensor
                    mytemp = ((mytemp - 4) * 9 / 5) + 32
                    mytemp = str(round(mytemp, 2))
                    mytemp = mytemp + "F"
                    # $ Get pressure reading from sensor.
                    mypres = sensor.data.pressure
                    mypres = str(round(mypres, 2))
                    mypres = mypres + "hPa"
                    # $ Get humidity reading from sensor.
                    myhumid = sensor.data.humidity
                    myhumid = str(round(myhumid, 2))
                    myhumid = myhumid + "% RH"
            if today_time != today_last_time:  # * Run once per cycle
                if sensor.data.heat_stable:  # ? Is the gas sensor heater stabilized?
                    # $ Get gas reading from sensor.
                    gas = sensor.data.gas_resistance
                    gas_offset = gas_baseline - gas
                    # TODO Don't get a humidity reading twice, use the previous one.
                    hum = sensor.data.humidity
                    hum_offset = hum - hum_baseline
                    # * Calculate hum_score as the distance from the hum_baseline.
                    if hum_offset > 0:
                        hum_score = 100 - hum_baseline - hum_offset
                        hum_score /= 100 - hum_baseline
                        hum_score *= hum_weighting * 100
                    else:
                        hum_score = hum_baseline + hum_offset
                        hum_score /= hum_baseline
                        hum_score *= hum_weighting * 100
                    # * Calculate gas_score as the distance from the gas_baseline.
                    if gas_offset > 0:
                        gas_score = gas / gas_baseline
                        gas_score *= 100 - (hum_weighting * 100)
                    else:
                        gas_score = 100 - (hum_weighting * 100)
                    #! Calculate air_quality_score.
                    air_quality_score = hum_score + gas_score
                    air_quality_score = round(air_quality_score, 2)
                    air_quality_score = str(air_quality_score) + "% AQI"
                today_last_time = today_time
                #! Read the data file for odroid, parse and format its data.
                oddata = open(f"{SCRIPT_PATH}/odroid-data", "r")
                for line in oddata:
                    if "," in line:
                        oddoutput = str(line)
                oddata.close()
                oddnums = re.findall("\d*\.?\d+", oddoutput)
                # $ Get the odroid cpu speed reading from datafile
                oddspeed = oddnums[3]
                # $ Get the odroid cpu temperature reading from datafile
                oddtemp = oddnums[4]
                oddtemp = float(oddtemp)
                foddtemp = round(oddtemp * 9 / 5 + 32)
                oddtemp = round(oddtemp)
                str_temp = str(oddtemp) + "C" + "/" + str(foddtemp) + "F"
                str_speed = str(oddspeed) + "Mhz"
                #! Acquire the local system data and format it.
                ltemp = 0
                process = Popen(
                    ["vcgencmd", "measure_temp"], stdout=PIPE
                )  # * Get the local cpu data
                output, _error = process.communicate()
                output = output.decode()
                pos_start = output.index("=") + 1
                pos_end = output.rindex("'")
                # $ Read the local cpu temp from vcgencmd
                ltemp = float(output[pos_start:pos_end])
                str_ltemp = "CPU: " + str(ltemp) + "C"
                # TODO: Use or remove fahrenheit calulating code
                # //fltemp = round(ltemp * 9 / 5 + 32, 1)
                # //str_fltemp = '    ' + str(fltemp) + 'F'
                #! Build and draw the canvas for on the OLED panel
                with canvas(device, dither=True) as draw:
                    logger.debug("Started OLED panel canvas draw.")
                    FontTemp = ImageFont.truetype(f"{SCRIPT_PATH}/fonts/code2000.ttf", 22)
                    now = datetime.datetime.now()
                    today_date = now.strftime("%d %b %y")
                    margin = 4
                    cx = 30
                    # TODO: Optionally change these 64s to 128s and cx=device.height/2 to make a fullscreen clock
                    cy = min(device.height, 64) / 2
                    left = cx - cy
                    right = cx + cy
                    # ! Build an analog clock
                    hrs_angle = 270 + (30 * (now.hour + (now.minute / 60.0)))
                    hrs = posn(hrs_angle, cy - margin - 7)
                    min_angle = 270 + (6 * now.minute)
                    mins = posn(min_angle, cy - margin - 2)
                    sec_angle = 270 + (6 * now.second)
                    secs = posn(sec_angle, cy - margin - 2)
                    draw.ellipse(
                        (
                            left + margin,
                            margin,
                            right - margin,
                            min(device.height, 64) - margin,
                        ),
                        outline="white",
                    )
                    # ! Draw
                    draw.line((cx, cy, cx + hrs[0], cy + hrs[1]), fill="white")
                    draw.line(
                        (cx, cy, cx + mins[0], cy + mins[1]), fill="white"
                    )  # ! an
                    # ! analog
                    draw.line((cx, cy, cx + secs[0], cy + secs[1]), fill="white")
                    draw.ellipse(
                        (cx - 2, cy - 2, cx + 2, cy + 2), fill="white", outline="white"
                    )  # ! clock
                    # ! Draw a digital clock in a fancy font
                    draw.text(
                        (2 * (cx + margin), 0), short_time, fill="white", font=FontTemp
                    )
                    draw.text(
                        (2 * (cx + margin), cy - 8), today_date, fill="white"
                    )  # ! Draw Date
                    draw.text(
                        (2 * (cx + margin), cy), today_time, fill="white"
                    )  # ! Draw Small clock
                    draw.text(
                        (2 * (cx + margin), cy + 8), mytemp, fill="white"
                    )  # ! Draw sensor Temperature
                    draw.text(
                        (2 * (cx + margin), cy + 16), mypres, fill="white"
                    )  # ! Draw sensor Pressure
                    draw.text(
                        (2 * (cx + margin), cy + 24), myhumid, fill="white"
                    )  # ! Draw sensor Humidity
                    if (
                        gas_baseline != 0
                    ):  # ? Is the sensor warmed up and giving accurate data?
                        # ! Draw sensor Air Quality Score
                        draw.text(
                            (2 * (cx + margin), cy + 32),
                            air_quality_score,
                            fill="white",
                        )
                        draw.text((0, cy + 32), "Forcast:", fill="white")
                        draw.text((0, cy + 40), "3 hr:", fill="white")
                        # ! Draw current conditions
                        draw.text((0, cy + 48), cur_condi, fill="white")
                        draw.text((0, cy + 56), "24 hr:", fill="white")
                        # ! Draw 24hr average conditions
                        draw.text((0, cy + 64), condi, fill="white")
                        # ! Draw forcast Temperature
                        draw.text((0, cy + 72), owm_temp, fill="white")
                        # ! Draw forcast Humidity
                        draw.text((0, cy + 80), owm_humid, fill="white")
                    else:  # ? Sensor not warmed up yet?
                        draw.text(
                            (5, cy + 32), "Retreiving data..", fill="white"
                        )  # * Draw waiting.. text
                    draw.text(
                        (2 * (cx + margin), cy + 40), str_ltemp, fill="white"
                    )  # ! Draw local cpu Temperature
                    # //draw.text((2 * (cx + margin), cy + 48), str_fltemp, fill='white')
                    draw.text((2 * (cx + margin), cy + 64), "Plex:", fill="white")
                    draw.text(
                        (2 * (cx + margin), cy + 72), str_speed, fill="white"
                    )  # ! Draw Plex cpu Temperature
                    draw.text(
                        (2 * (cx + margin), cy + 80), str_temp, fill="white"
                    )  # ! Draw Plex cpu Speed
                    # & Log the canvas draw completion -wink-
                    logger.debug("Completed OLED Panel canvas draw.")
            # ! Wait the specified refresh time before resetting the loop
            time.sleep(REFRESH_TIME)
        except:
            #! This isn't really error catching, we are just ignoring them and going again.
            #! The assumption is that any errors will be temporary and subsequent runs will function.
            # TODO: Handle errors better so we can log with more detail and retain more data from what IS working.
            logger.debug("An exception occurred during the refresh!")
            #! !!! The above logging level was changed to stop a bug which filled the
            #! !!! syslog and daemom.log files until the system storage was all used.
            pass


if __name__ == "__main__":
    try:
        # $ Set the i2c serial settings for the oled panel
        serial = i2c(port=1, address=0x3C)
        # $ Set the model, size, and rotation of the oled panel
        device = sh1106(serial, rotate=2, width=128, height=128, mode="1")
        # $ Set the oled panel brightness to default.
        change_brightness(SCREEN_BRIGHTNESS)
        sensor = bme680.BME680()  # $ Load up the environmental sensor
        owm_running = False
        if CAN_INTERNET == True:  # ? Is there internet access?
            # Set the API key
            owm = pyowm.OWM("dcf3760c23dca5b013656cad67f6d72a")
            # ? If the API didn't work, there's prolly no internet.
            CAN_INTERNET = owm.is_API_online()
            # //do_weather()
    except KeyboardInterrupt:  # ! Catch user exit
        logger.warning("User triggered exit.")
        pass
    except:
        logger.error("An exception occurred during startup!")
        pass
    main()

# TODO: Fix or remove this code for finding most frequent strings.
# //         str_gonna_rain = 'no rain'
# //            precips = ['no rain']
# //            x = 0
# //            if fc.will_have_rain() == True:
# //                f = fc.when_rain()
# //                for weather in f:
# //                    x = x + 1
# //                    if x == 10:
# //                        break
# //                    if weather.get_detailed_status != 'light rain':
# //                    precips.append(str(weather.get_detailed_status()))
# //                str_gonna_rain = most_frequent(precips)
# //            x = 0
# //            if fc.will_have_snow() == True:
# //                f = fc.when_snow()
# //                for weather in f:
# //                    x = x +1
# //                    if x == 10:
# //                        break
# //                    precips.append(str(weather.get_detailed_status()))
# //            print(precips)
# //            str_gonna_rain = most_frequent(precips)
# //            logger.info(f'Predicted rain: {str_gonna_rain}')
