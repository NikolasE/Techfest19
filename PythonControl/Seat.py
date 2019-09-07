#!/usr/bin/env python3
# *-*- coding: utf-8 -*-

import serial
import threading


class Seat():
    def __init__(self, serial_port='/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0', baud_rate=230400):
        self._serial = serial.Serial(port=serial_port, baudrate=baud_rate)
        if not self._serial.isOpen():
            raise RuntimeError("Couldn't open %s" % serial_port)
        self.mm = 0
        self._ser_thread = threading.Thread(
            target=self._read_thread, daemon=True)
        self._ser_thread.start()

    def _read_thread(self):
        while True:
            data = self._serial.readline()
            if data:
                s = str(data)[2:][:-5]
                try:
                    trans = float(s)
                    self.mm = trans*0.03 + 200
                except ValueError:
                    pass

    def get_mm(self):
        return self.mm
