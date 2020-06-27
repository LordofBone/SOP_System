#!/usr/bin/env python

# imports
import os
import threading
from time import sleep

import RPi.GPIO as GPIO
import qprompt

from ammo_counter import ammoshow
from display_out import set_row_1
from environment_sensor import get_env_data
from fingerprint_worker import deleteprint, get_num, enroll_finger, \
    number_store
from gps_runner3 import get_coords
from heart_check import HeartMonitor
from locker import clear_servo
from range_runner import rangeget
from sop_user_login import login, logout, logout_offcheck, unconditional_login

# on run of script ensure the blaster is locked
logout()

# setup menu library
menu = qprompt.Menu()

# set current user count - doesn't appear to work properly, will have to figure out why (always returns 0)
current_user_count = number_store()

# get user count and +1 if there is already a user registered, so that the next registration adds a user
# the get number function for amount of registered users in the fingerprint sensor doesn't work at the moment though
try:
    if not current_user_count == 0:
        next_user_no = get_num(current_user_count + 1)
    else:
        next_user_no = 0
except ValueError:
    next_user_no = 0
    print("Max users reached, next user ID is set to 0. NEXT ENROLL WILL ERASE THE FIRST ENROLLED USER.")

# start heartrate monitor interface class
getbeat = HeartMonitor()

# start the monitor
getbeat.startbeat()


# remove all users from the fingerprint sensor
def remove_allusers():
    for i in range(127):
        deleteprint(i)


# show usercount to the admin (as above this always returns 0 for some reason)
def show_usercount():
    print(number_store())


# cleardown function
def clearthings():
    clear_servo()
    GPIO.cleanup()
    getbeat.stopbeat()


# shutdown function
def shutdown():
    clearthings()
    os.system("sudo shutdown now")


# show ammo function
def getammo():
    print("Ammo remaining: ", ammoshow(), "Darts")


# show environment data function
def getenvironment():
    print(get_env_data())


# reboot function
def reboot():
    clearthings()
    os.system("sudo reboot now")


# get heartrate function
def get_rate():
    print("User Heartrate: ", getbeat.getheartrate(), "BPM")


# get muzzle range function
def get_range():
    print("Distance:", rangeget(), "CM")


# get gps location function
def get_gps():
    print("User GPS: ", get_coords(), " Coordinates")


# logout function
def lockout():
    logout()


# add user function, displays to the user to place their finger for registration
def add_user(new_id):
    set_row_1("Enroll")

    sleep(3)

    set_row_1("Place finger")

    if enroll_finger(new_id):
        set_row_1("Enroll SUCCESS")
        print("Successfully enrolled user")
    else:
        set_row_1("Enroll FAIL")
        print("Failed to enroll user, check above messages for reason")


# loop for locking blaster if a pulse is no longer detected (for example if the blaster is put down or dropped)
def heartlogout():
    while True:
        if getbeat.getheartrate() == 0:
            logout_offcheck()
            sleep(10)


def login_user():
    if not getbeat.getheartrate() == 0:
        loginsuccess, loginid = login()

        if loginsuccess:
            print("User" + str(loginid) + "Logged In")
        else:
            print("User Login Failed")
    else:
        logout()
        print("No pulse detected.")


# start thread for pulse detection loop - threading is used so that the program can continue to work alongside
# the loop
run_h = threading.Thread(target=heartlogout, args=())
run_h.start()

# menu setup and display
try:
    menu.add("1", "Get Heart Rate", get_rate)
    menu.add("2", "Show Ammo Count", getammo)
    menu.add("3", "Show Environment Data", getenvironment)
    menu.add("4", "Show Muzzle Range", get_range)
    menu.add("5", "Show GPS Location", get_gps)
    menu.add("6", "Lock Immediately", lockout)
    menu.add("7", "Unlock Immediately (No ID required)", unconditional_login)
    menu.add("8", "Add User", add_user, [next_user_no])
    menu.add("9", "Remove ALL Users", remove_allusers)
    menu.add("10", "Show User Count", show_usercount)
    menu.add("11", "Prompt User Login", login_user)
    menu.add("12", "Reboot", reboot)
    menu.add("13", "Shutdown", shutdown)
    menu.main(loop=True)
except KeyboardInterrupt:
    clearthings()
