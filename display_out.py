#!/usr/bin/env python

# requires RPi_I2C_driver.py

# imports
import threading
from time import *

import RPi_I2C_driver

# setup global variables
text_row_1 = ""
text_row_2 = ""


# set global string here for row 1
def set_row_1(text_in):
    global text_row_1
    text_row_1 = text_in


# set global string here for row 2
def set_row_2(text_in):
    global text_row_2
    text_row_2 = text_in


# grab latest content of global row 1 and row 2 variables, clear screen and write them to the screen
# done this way so that the contents of one row can change without changing the other
def draw_screen():
    global text_row_1
    global text_row_2
    while True:
        clear()
        mylcd.lcd_display_string_pos(str(text_row_1), 1, 0)  # row 1, column 0
        mylcd.lcd_display_string_pos(str(text_row_2), 2, 0)  # row 2, column 0
        sleep(1)


# backlight controls don't seem to work, but this function is for turning the backlight on
def backlight_on():
    mylcd.backlight(1)


# backlight controls don't seem to work, but this function is for turning the backlight off
def backlight_off():
    mylcd.backlight(0)


# clear lcd function
def clear():
    mylcd.lcd_clear()


# setup lcd
mylcd = RPi_I2C_driver.lcd()
# run a boot-test
backlight_on()
mylcd.lcd_display_string("RPi I2C test", 1)
mylcd.lcd_display_string("!£$%^&*(){}:@~<>?,", 2)

# 1 second delay and clear
sleep(1)

clear()

# display initialisation message and clear
mylcd.lcd_display_string("SOP System", 1)
mylcd.lcd_display_string("INITIALISED", 2)

sleep(5)

backlight_off()

clear()

# setup a thread for drawing to the screen
run_h = threading.Thread(target=draw_screen, args=())
run_h.start()
