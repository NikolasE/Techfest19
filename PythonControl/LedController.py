#!/usr/bin/env python3
# *-*- coding: utf-8 -*-

import serial
import struct


class LedController():

    _CMD_RESET = b'r'
    _CMD_SEAT = b's'
    _CMD_CHAIN = b'c'
    _CMD_VEL = b'v'
    _CMD_DIST = b'd'
    _CMD_SETP_SEAT = b'S'
    _CMD_SETP_CHAIN = b'C'

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
        self.reset_leds()

    def reset_leds(self):
        """reset all leds to black/off"""
        cmd = self._CMD_RESET + b'\n'
        self._serial.write(cmd)

    def set_seat(self, val):
        """set seat led strips. value: 0-60"""
        if val < 0 or val > 60:
            return
        cmd = self._CMD_SEAT + struct.pack('B', val) + b'\n'
        self._serial.write(cmd)

    def set_seat_setpoint(self, val):
        """set seat setpoint led. value: 0-60"""
        if val < 0 or val > 60:
            return
        cmd = self._CMD_SETP_SEAT + struct.pack('B', val) + b'\n'
        self._serial.write(cmd)

    def set_chain(self, val):
        """set chain led strip. value: 0-60"""
        if val < 0 or val > 60:
            return
        cmd = self._CMD_CHAIN + struct.pack('B', val) + b'\n'
        self._serial.write(cmd)

    def set_chain_setpoint(self, val):
        """set chain setpoint led. value: 0-60"""
        if val < 0 or val > 60:
            return
        cmd = self._CMD_SETP_CHAIN + struct.pack('B', val) + b'\n'
        self._serial.write(cmd)

    def set_vel(self, val):
        """set velocity led strip bright part. value: 0-255"""
        if val < 0 or val > 255:
            return
        cmd = self._CMD_VEL + struct.pack('B', val) + b'\n'
        self._serial.write(cmd)

    def set_dist(self, val):
        """set velocity led strip blue part. value: 0-60"""
        if val < 0 or val > 60:
            return
        cmd = self._CMD_DIST + struct.pack('B', val) + b'\n'
        self._serial.write(cmd)


if __name__ == '__main__':
    num_leds = 60 * 4
    ledController = LedController(num_leds=num_leds)

    import IPython
    IPython.embed()
