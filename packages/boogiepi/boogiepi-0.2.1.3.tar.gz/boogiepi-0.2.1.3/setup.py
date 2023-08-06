import setuptools
from setuptools import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="boogiepi",
    version="0.2.1.3",
    author="Chris Laprade",
    author_email="chris@boogiemobile.net",
    description="Sensor data processing and visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BoogieMobile/boogiepi",
    packages=setuptools.find_packages(),
    license="A-GPLv3",
    classifiers=[
        #"Description-Content-Type: text/markdown; charset=UTF-8; variant=GFM",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)