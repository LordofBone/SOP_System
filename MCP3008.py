#!/usr/bin/env python

# from https://github.com/tutRPi/Raspberry-Pi-Heartbeat-Pulse-Sensor

# imports
from spidev import SpiDev


class MCP3008:
    def __init__(self, bus=0, device=0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()

    def open(self):
        self.spi.open(self.bus, self.device)
        # doesn't seem to work without this
        # https://www.takaitra.com/spi-device-raspberry-pi/
        self.spi.max_speed_hz = 1350000

    def read(self, channel=0):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def close(self):
        self.spi.close()
