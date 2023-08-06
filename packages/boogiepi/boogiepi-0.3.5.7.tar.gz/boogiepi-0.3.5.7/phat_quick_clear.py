# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


#! WARNING: This script is mostly deprecated by assasinatour
#! It is being kept for the time being until all compatibility
#! issues have been marked, sorted, and resolved. -Chris

import ledshim
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import sh1106


def clearoled():
    serial = i2c(port=1, address=0x3C)
    device = sh1106(serial, rotate=2, width=128, height=128, mode="1")
    device.clear()
    device.hide()


def clearshim():
    ledshim.clear()
    ledshim.show()


def run():
    clearoled()
    clearshim()


def main():
    run()


if __name__ == '__main__':
    main()
