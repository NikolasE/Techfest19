#!/usr/bin/env python3
# *-*- coding: utf-8 -*-

import serial
import numpy as np
import struct


class LedController():
    def __init__(self, serial_port='/dev/serial/by-id/usb-SparkFun_LEDController-if00', baud_rate=1000000, num_leds=60*4):
        """Connects to the microcontroller on a serial port.
        Args:
            port: The serial port or path to a serial device.
            baud_rate: The bit rate for serial communication.
        Raises:
            ValueError: There is an error opening the port.
            SerialError: There is a configuration error.
        """
        self._serial = serial.Serial(port=serial_port, baudrate=baud_rate)
        if not self._serial.isOpen():
            raise RuntimeError("Couldn't open %s" % serial_port)
        self._pixels = np.array([(0, 0, 0, 0)]*num_leds)
        self._bytes = np.zeros(num_leds*4)

    def set_led(self, number, color):
        assert len(color) == 4

        """Sets as specific led to the given color; color is a 4-tuple (R,G,B,W)"""
        cmd = struct.pack('>hBBBB', number,
                          color[0], color[1], color[2], color[3])
        self._serial.write(cmd + b'\n')

    # def prepare_led(self, cmd, number, color):
    #     """Sets as specific led to the given color; color is a 4-tuple (R,G,B,W)"""
    #     cmd += struct.pack('>hBBBB', number,
    #                        color[0], color[1], color[2], color[3])
    #     return cmd + b'\n'

    # def send_prepared(self, cmd):
    #     self._serial.write(cmd)


if __name__ == '__main__':
    num_leds = 60 * 4
    ledController = LedController(num_leds=num_leds)
    for i in range(0, num_leds):
        ledController.set_led(i, (0, 0, 255, 0))

    import IPython
    IPython.embed()
