#!/usr/bin/env python

# imports
from pulsesensor import Pulsesensor


# class for interfacing with the pulsesensor code easier
class HeartMonitor:

    def __init__(self):
        self.p = Pulsesensor()

    def startbeat(self):
        self.p.startAsyncBPM()

    def getheartrate(self):
        return self.p.BPM

    def stopbeat(self):
        self.p.stopAsyncBPM()
