#!/usr/bin/env python

# imports
import time

import RPi.GPIO as GPIO

# general imports

# setup for the GPIO
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


# loop for measuring distance, this fires out a pulse and measures time to return, it then converts to an int to
# remove decimals and- finally to a string to be sent to the admin module
def rangeget():
    # print "Distance Measurement In Progress"

    GPIO.output(TRIG, False)
    # print "Waiting For Sensor To Settle"
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = int(distance)

    distance = str(distance)

    return distance
