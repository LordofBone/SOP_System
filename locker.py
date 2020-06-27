#!/usr/bin/env python

# imports
from time import sleep

import RPi.GPIO as GPIO

from display_out import set_row_1

# setup GPIO
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

# GPIO 17 for PWM with 50Hz
p = GPIO.PWM(servoPIN, 50)

# lock/unlock servo positions
lockposition = 5.5
unlockposition = 6.2

p.start(lockposition)


# function to move servo to lock position and set display to "LOCKED"
def lock():
    p.ChangeDutyCycle(lockposition)
    set_row_1("LOCKED")
    sleep(0.5)


# function to move servo to unlock position and set display to "UNLOCKED"
def unlock():
    p.ChangeDutyCycle(unlockposition)
    set_row_1("UNLOCKED")
    sleep(0.5)


# function to clear GPIO and stop servo controls
def clear_servo():
    lock()
    p.stop()
    GPIO.cleanup()
