#!/usr/bin/env python

# imports
import threading
from dataclasses import dataclass
from time import sleep

import Adafruit_VCNL40xx
import RPi.GPIO as GPIO

from display_out import set_row_2

# the proximity sensor
vcnl = Adafruit_VCNL40xx.VCNL4010()

# touch button
reload_channel = 16

# setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(reload_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# the class used for counting the shots up/down and resetting
@dataclass
class AdjustShots(object):
    shot_n: int

    def change_ammo(self, shot_n):
        self.shot_n = shot_n
        return self.shot_n

    def show_ammo(self):
        return self.shot_n

    def plus_shots(self):
        if self.shot_n < 20:
            self.shot_n = self.shot_n + 1
        else:
            self.shot_n = (-0)
        return self.shot_n

    def minus_shots(self):
        if not self.shot_n < 0:
            self.shot_n = self.shot_n - 1
        return self.shot_n


# here we set the number of shots that are currently in the magazine (0 is -1 here as the counter works by 0 indexing)
shotsMag = AdjustShots(-1)
# here we set the default number of shots per magazine that will be used (as above 11 will count as 12 due to 0
# indexing)
shotsPerMag = AdjustShots(5)


# set row 2 of the display to current shots
def display_shots(shot_count):
    set_row_2("Ammo: " + str(shot_count))


# show current ammo to the admin
def ammoshow():
    return shotsMag.show_ammo()


# function for calling the class to minus shots from the current magazine
def shot_detected():
    shotsMag.minus_shots()


# the touch button initiates a 'reload', so when you put a mag in or reload it will reset the counter to show remaining
# ammo in the current mag
def reload(reloaded):
    shotsMag.change_ammo(shotsPerMag.show_ammo())
    display_shots(shotsMag.show_ammo())
    sleep(1)


# loop for detecting proximity - proximity decreasing when a shot passes the sensor indicating a shot and calling the
# class for the current magazine to minus one shot
def shot_sensor():
    while True:
        proximity = vcnl.read_proximity()

        if proximity > 2540:
            shot_detected()
            display_shots(shotsMag.show_ammo())
            sleep(1)


# uses event detect to grab button press event without having to use a loop
GPIO.add_event_detect(reload_channel, GPIO.FALLING, callback=reload, bouncetime=100)

# the function for sensing shots is threaded so that the program can continue doing other things while waiting for a
# shot
run1 = threading.Thread(target=shot_sensor, args=())
run1.start()
