# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import matplotlib.pyplot as plt
import numpy as np

f = np.loadtxt('coordinates.txt', delimiter=' ', skiprows=1)

f = f[f[:, 2] == 1]
x = f[:, 0]
y = f[:, 1]
plt.plot([x], [y], 'ro')
plt.show()
