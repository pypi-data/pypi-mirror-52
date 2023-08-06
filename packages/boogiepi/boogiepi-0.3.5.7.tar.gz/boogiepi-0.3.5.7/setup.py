# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Chris Laprade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import setuptools
from setuptools import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="boogiepi",
    version="0.3.5.7",
    python_requires='>=3.6',
    author="Chris Laprade",
    author_email="chris@boogiemobile.net",
    description="Sensor data processing and visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BoogieMobile/boogiepi",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",

    ],
)