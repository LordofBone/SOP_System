#!/usr/bin/env python

# imports
from time import sleep

from display_out import set_row_1
from fingerprint_worker import getprint
from locker import lock, unlock

# switch for determining whether the SOP system is de-activated
sop_off = False


# authorise user via fingerprint and unlock if fingerprint recognised
def login():
    global sop_off
    sop_off = False
    lock()
    set_row_1("Login")

    sleep(3)

    set_row_1("Place finger")

    success, userid = getprint()

    if not success:
        lock()
        set_row_1("Access DENIED")
    else:
        unlock()
        set_row_1("USR: " + str(userid) + " UNLOCKED")

    return success, userid


# unlock and set SOP to disabled, requiring no user authorisation via fingerprint
def unconditional_login():
    unlock()
    set_row_1("SOP DISABLED")
    global sop_off
    sop_off = True


# log user out (lock blaster)
def logout():
    global sop_off
    sop_off = False
    lock()


# logout function does the same as above except that if its called while SOP is disabled it will not logout
# this is the function that is called by the heartrate loop in the sop admin module when a pulse is no longer detected
# when SOP is disabled and the pulse is no longer detected this won't lock the blaster, keeping the blaster
# unconditionally locked
def logout_offcheck():
    global sop_off
    if not sop_off:
        lock()
