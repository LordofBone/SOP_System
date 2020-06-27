#!/usr/bin/env python
# from https://ozzmaker.com/using-python-with-a-gps-receiver-on-a-raspberry-pi/

# imports
from gps import *

running = True


def get_coords():
    gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
    nx = gpsd.next()
    # For a list of all supported classes and fields refer to:
    # https://gpsd.gitlab.io/gpsd/gpsd_json.html
    if nx['class'] == 'TPV':
        latitude = getattr(nx, 'lat', "Unknown")
        longitude = getattr(nx, 'lon', "Unknown")
        # print("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
        return "lon = " + str(longitude) + ", lat = " + str(latitude)
