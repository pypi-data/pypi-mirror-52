# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import time

import ledshim
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import sh1106

serial = i2c(port=1, address=0x3C)
device = sh1106(serial, rotate=2, width=128, height=128, mode="1")
device.contrast(255)

with canvas(device, dither=True) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="white")
while True:
    try:
        time.sleep(1)
    except:
        #! This will run on exit
        device.cleanup()
        ledshim.clear()
        break
